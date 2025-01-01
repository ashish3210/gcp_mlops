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

# +
from google.cloud import bigquery
import pandas as pd

def bq2pd(PROJECT_ID:str, DATASET_ID:str, TABLE_ID)->pd.DataFrame:
    
    client = bigquery.Client()

    # Define your SQL query
    query = f"""
    SELECT * 
    FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
    """

    # Execute the query and fetch data into a Pandas DataFrame
    df = client.query(query).to_dataframe()
    
    return df
