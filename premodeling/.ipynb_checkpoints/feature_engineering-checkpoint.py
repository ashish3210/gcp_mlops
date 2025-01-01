# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.4
#   kernelspec:
#     display_name: Python 3 (ipykernel) (Local)
#     language: python
#     name: conda-base-py
# ---

from google.cloud import bigquery
from config import *
import pandas as pd


# +
def extract_features(PROJECT_ID:str, DATASET_ID:str, TABLE_ID:str) -> pd.DataFrame:
    """
    Extracts features from the 'date' column in the dataframe.
    Features: 'month', 'weekend' (1 if weekend, 0 if weekday)
    
    Args:
    - df (pd.DataFrame): The input dataframe with a 'date' column
    
    Returns:
    - pd.DataFrame: A dataframe with 'month' and 'weekend' features added
    """
    logging.info('feature creation started')
    df = bq2pd(PROJECT_ID, DATASET_ID, TABLE_ID)
    
    # Ensure 'date' column is in datetime format
    df['date'] = pd.to_datetime(df['date'])

    # Extract month from the 'date' column
    df['month'] = df['date'].dt.month

    # Extract weekend: 1 if weekend (Saturday/Sunday), 0 if weekday (Mon-Fri)
    df['weekend'] = df['date'].dt.weekday >= 5  # Saturday and Sunday are >= 5

    # Convert boolean weekend column to 1/0
    df['weekend'] = df['weekend'].astype(int)
    logging.info('features created')
    return df

if __name__ == "__main__":
    extract_features(PROJECT_ID, DATASET_ID, TABLE_ID)

