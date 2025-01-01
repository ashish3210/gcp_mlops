import pandas as pd
import logging
from google.cloud import bigquery
from config import PROJECT_ID, DATASET_ID, TABLE_ID, CSV_FILE_PATH


def load_csv_to_bigquery(file_path, project_id, dataset_id, table_id):
    """
    Load a CSV file into BigQuery.
    """
    logging.info('ingestion started')
    client = bigquery.Client(project=project_id)

    # Read CSV into a DataFrame
    print(f"Reading data from {file_path}...")
    df = pd.read_csv(file_path)

    # Load DataFrame to BigQuery
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        source_format=bigquery.SourceFormat.CSV,
        autodetect=True,  # Auto-detect schema
    )
   
    job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    job.result()  # Wait for the job to complete
    logging.info(f"ingested to {table_ref}...")



if __name__ == "__main__":
    load_csv_to_bigquery(CSV_FILE_PATH, PROJECT_ID, DATASET_ID, TABLE_ID)
