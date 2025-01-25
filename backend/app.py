from flask import Flask, request, jsonify
import numpy as np
import os
from dotenv import load_dotenv
import mlflow
import mlflow.pyfunc
from flask_cors import CORS

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
    """Preload the model from MLflow during app startup."""
    global loaded_model
    try:
        # Fetch the latest model version from MLflow Model Registry
        client = mlflow.tracking.MlflowClient()

        # Get all versions of the model
        versions = client.get_registered_model(MODEL_NAME).latest_versions

        # Sort the versions to get the latest one (by version number)
        latest_version = sorted(versions, key=lambda v: v.version, reverse=True)[0]

        # Load the latest model
        model_uri = f"models:/{MODEL_NAME}/{latest_version.version}"
        loaded_model = mlflow.pyfunc.load_model(model_uri)
        print(f"Model version {latest_version.version} loaded successfully from MLflow!")
    except Exception as e:
        print(f"Error loading model from MLflow: {str(e)}")
        raise


@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction requests."""
    try:
        global loaded_model

        if loaded_model is None:
            raise ValueError("Model not loaded. Please check server logs for errors during model initialization.")

        # Get the data from the request
        data = request.get_json()

        # Extract input values from the JSON request
        area = float(data.get('area', 0))
        bedrooms = float(data.get('bedrooms', 0))
        bathrooms = float(data.get('bathrooms', 0))
        stories = float(data.get('stories', 0))
        mainroad = 1 if data.get('mainroad', '').lower() == 'yes' else 0
        guestroom = 1 if data.get('guestroom', '').lower() == 'yes' else 0
        basement = 1 if data.get('basement', '').lower() == 'yes' else 0
        hotwaterheating = 1 if data.get('hotwaterheating', '').lower() == 'yes' else 0
        airconditioning = 1 if data.get('airconditioning', '').lower() == 'yes' else 0

        # Combine all features into a single input array
        input_features = np.array([area, bedrooms, bathrooms, stories, mainroad, guestroom, basement, hotwaterheating, airconditioning]).reshape(1, -1)

        # Make prediction using the model
        predicted_price = loaded_model.predict(input_features)[0]

        # Return the predicted price as JSON
        return jsonify({"predicted_price": round(predicted_price, 2)})

    except Exception as e:
        # Return error response if an exception occurs
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    # Preload the model when the server starts
    preload_model()
    app.run(debug=True, host='0.0.0.0', port=8000)
