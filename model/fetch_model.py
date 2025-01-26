import mlflow
from mlflow.tracking import MlflowClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MLflow Tracking URI from .env
MLFLOW_TRACKING_URI = os.getenv('MLFLOW_TRACKING_URI')

# Set the MLflow Tracking URI
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# Initialize the MLflow client
client = MlflowClient()

# Function to fetch the latest model in the Production stage
def fetch_production_model():
    try:
        # fetch the model in production stage
        registered_models = client.search_registered_models()
        
        for model in registered_models:
            # Check all versions of the model for the Production stage
            production_versions = client.get_latest_versions(model.name, stages=["Production"])
            print(f"Model: {model.name}, Versions: {production_versions}")
            
            if production_versions:
                # Get the latest version saved as Production
                latest_version = max(production_versions, key=lambda v: v.version)
                print(f"Latest Production Version: {latest_version.version}")
                model_name = model.name
                print(f"Model Name: {model_name}")
                model_uri = latest_version.source  # Use the source URI directly
                print(f"Model URI: {model_uri}")

                # Define a local path to download the model
                local_path = f"models/{model_name}"
                os.makedirs(local_path, exist_ok=True)
                # does the path exit ?
                print(f"Path Exists: {os.path.exists(local_path)}")
                print(f"Local Path: {local_path}")

                # Download the model artifacts to the local directory
                mlflow.artifacts.download_artifacts(artifact_uri=model_uri, dst_path=local_path)

                print(f"Model '{model_name}' version {latest_version.version} in Production downloaded successfully to {local_path}")
                return local_path, model_name  # Return the local path and model name for further use

        raise Exception("No models found in the Production stage.")
    except Exception as e:
        print(f"Error fetching the model: {str(e)}")
        raise

# Fetch the latest model in the Production stage
fetch_production_model()