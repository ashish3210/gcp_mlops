import pandas as pd
import pickle
import logging
from prophet import Prophet
from google.cloud import storage
from io import BytesIO
from config import *

def train_model(df: pd.DataFrame, gcs_bucket_name: str, gcs_model_path: str) -> None:
    """
    Train a Prophet model on the given data and save the model directly to Google Cloud Storage.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing the training data with 'ds' and 'y' columns.
        gcs_bucket_name (str): Name of the GCS bucket to upload the trained model.
        gcs_model_path (str): Path within the GCS bucket to save the trained model.
    """
    logging.info(f"training started'")
    # Ensure the required columns exist
    if 'ds' not in df.columns or 'y' not in df.columns:
        raise ValueError("The dataset must have 'ds' and 'y' columns for Prophet.")

    # Train the Prophet model
    model = Prophet()
    model.fit(df)

    # Serialize the model to bytes
    model_bytes = BytesIO()
    pickle.dump(model, model_bytes)
    model_bytes.seek(0)  # Reset the buffer position to the beginning

    # Upload the serialized model to GCS
    client = storage.Client()
    bucket = client.bucket(gcs_bucket_name)
    blob = bucket.blob(gcs_model_path)

    blob.upload_from_file(model_bytes, content_type='application/octet-stream')
    logging.info(f"Model uploaded to GCS bucket '{GCS_BUCKET}' with blob name '{GCS_MODEL_PATH}'")
    
    return model

