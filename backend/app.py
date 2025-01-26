from flask import Flask, request, jsonify
import numpy as np
import os
from dotenv import load_dotenv
import mlflow
import mlflow.pyfunc
from flask_cors import CORS
from supabase_client import save_to_supabase

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# MLflow Tracking URI and model name from .env
MLFLOW_TRACKING_URI = os.getenv('MLFLOW_TRACKING_URI')
MLFLOW_EXPERIMENT_NAME = os.getenv('MLFLOW_EXPERIMENT_NAME')
MODEL_NAME = "LinearRegressionModel"

# Set MLflow tracking URI
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# Global variable to store the preloaded model
loaded_model = None


def preload_model():
    #load the model from directory
    global loaded_model
    try:
        # list the models inside the models folder
        local_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "backend", "models")
        model_name = os.listdir(local_path)[0]
        print(f"Model Name: {model_name}")

        #load the model using sklearn
        loaded_model = mlflow.sklearn.load_model(local_path + "/" + model_name)
        print("Model loaded successfully")

    except Exception as e:
        print(f"Error loading the model: {e}")


def preprocess_input(data):
    """
    Preprocess the input data from the front end to match the 23 features expected by the model.
    """
    # Initialize all features with default values
    features = {
        'area': int(data.get('area', 0)),
        'mainroad': 1 if data.get('mainroad', '').lower() == 'yes' else 0,
        'guestroom': 1 if data.get('guestroom', '').lower() == 'yes' else 0,
        'basement': 1 if data.get('basement', '').lower() == 'yes' else 0,
        'hotwaterheating': 1 if data.get('hotwaterheating', '').lower() == 'yes' else 0,
        'airconditioning': 1 if data.get('airconditioning', '').lower() == 'yes' else 0,
        'prefarea': 1 if data.get('prefarea', '').lower() == 'yes' else 0,
        'furnishingstatus_semi-furnished': 1 if data.get('furnishingstatus', '').lower() == 'semi-furnished' else 0,
        'furnishingstatus_unfurnished': 1 if data.get('furnishingstatus', '').lower() == 'unfurnished' else 0,
        'bathrooms_2': 1 if int(data.get('bathrooms', 0)) == 2 else 0,
        'bathrooms_3': 1 if int(data.get('bathrooms', 0)) == 3 else 0,
        'bathrooms_4': 1 if int(data.get('bathrooms', 0)) == 4 else 0,
        'stories_2': 1 if int(data.get('stories', 0)) == 2 else 0,
        'stories_3': 1 if int(data.get('stories', 0)) == 3 else 0,
        'stories_4': 1 if int(data.get('stories', 0)) == 4 else 0,
        'parking_1': 1 if int(data.get('parking', 0)) == 1 else 0,
        'parking_2': 1 if int(data.get('parking', 0)) == 2 else 0,
        'parking_3': 1 if int(data.get('parking', 0)) == 3 else 0,
        'bedrooms_2': 1 if int(data.get('bedrooms', 0)) == 2 else 0,
        'bedrooms_3': 1 if int(data.get('bedrooms', 0)) == 3 else 0,
        'bedrooms_4': 1 if int(data.get('bedrooms', 0)) == 4 else 0,
        'bedrooms_5': 1 if int(data.get('bedrooms', 0)) == 5 else 0,
        'bedrooms_6': 1 if int(data.get('bedrooms', 0)) == 6 else 0
    }

    # Convert the feature dictionary to a NumPy array for prediction
    input_array = np.array(list(features.values())).reshape(1, -1)
    return input_array


@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction requests."""
    try:
        global loaded_model

        if loaded_model is None:
            raise ValueError("Model not loaded. Please check server logs for errors during model initialization.")

        # Get the data from the request
        data = request.get_json()

        # Preprocess the data
        input_features = preprocess_input(data)

        # Make prediction using the model
        predicted_price = loaded_model.predict(input_features)[0]

        # Ensure the prediction is returned as an integer
        predicted_price_int = int(round(predicted_price))

        # Save prediction to Supabase
        save_to_supabase(data, predicted_price_int)

        # Return the predicted price as JSON
        return jsonify({"predicted_price": predicted_price_int})

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    # Preload the model when the server starts
    preload_model()
    app.run(debug=True, host='0.0.0.0', port=8000)