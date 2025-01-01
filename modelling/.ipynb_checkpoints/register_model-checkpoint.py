from google.cloud import aiplatform
from config import *
import logging

def register_model(model_path: str, display_name: str, project_id: str, region: str):
    """
    Registers a trained model in Vertex AI Model Registry.
    
    Parameters:
        model_path (str): GCS path where the trained model is saved (e.g., pickle or serialized format).
        display_name (str): Display name for the model in the registry.
        project_id (str): GCP Project ID.
        region (str): GCP Region where Vertex AI is used.
    
    Returns:
        model (aiplatform.Model): The registered model object.
    """
    logging.info('model registry started')
    aiplatform.init(project=project_id, location=region)

    # Register the model in Vertex AI
    model = aiplatform.Model.upload(
        display_name=display_name,
        artifact_uri=model_path,  # GCS path to the model directory
        serving_container_image_uri="us-docker.pkg.dev/vertex-ai/prediction/sklearn-cpu.1-0:latest",  # Prebuilt container
    )

    logging.info(f"Model registered with resource name: {model.resource_name}")
    return model


if __name__ == "__main__":
    register_model(GCS_MODEL_PATH, 'model_1', PROJECT_ID, REGION)