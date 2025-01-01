from kfp import dsl #
from kfp import compiler
from kfp.dsl import Input, Output, Dataset, Model
import google.cloud.aiplatform as aip
import pandas as pd


@dsl.component(base_image="python:3.10")
def data_ingestion(file_path: str, project_id: str, dataset_id: str, table_id: str, output_data: Output[Dataset]):
    import pandas as pd
    from premodeling.csv_to_bq import load_csv_to_bigquery
    from premodeling.feature_engineering import extract_features
    
    load_csv_to_bigquery(file_path, project_id, dataset_id, table_id)
    df = extract_features(project_id, dataset_id, table_id)
    
    df.to_csv(output_data.path, index=False)
    
@dsl.component
def modelling(input_data: Input[Dataset], model_output: Output[Model]):
    import pandas as pd
    from modelling.train import train_model
    from modelling.register_model import register_model
    
    df = pd.read_csv(input_data.path)
    train_model(df, gcs_bucket_name='kaggle-sale', gcs_model_path='kaggle-sales/models/prophet_model.pkl')
    register_model(model_path, display_name="forecasting-model", project_id="theta-maker-446106-s4", region="us-central1-a")
    
    with open(model_output.path, "w") as f:
        f.write(model_path)
    
@dsl.component
def inference(model: Input[Model], forecast_output: Output[Dataset]):
    import pandas as pd
    from inference.inference import predict
    
    forecast = predict(model_path=model.path, project_id="theta-maker-446106-s4", region="us-central")
    
    forecast.to_csv(forecast_output.path, index=False)
    


# Define the pipeline
@dsl.pipeline(
    name="kaggle-forecast",
    description="try pipeline"
)
def forecast_pipeline(file_path: str, project_id: str, dataset_id: str, table_id: str):
    data_task = data_ingestion(file_path=file_path,
        project_id=project_id,
        dataset_id=dataset_id,
        table_id=table_id)
    
    data_task.set_disk_size("10Gi")
    
    model_task = modelling(input_data=data_task.output)
    
    
    forecast = inference(model=model_task.output)


# Compile the pipeline
pipeline_file = "kaggle_pipeline.json"
compiler.Compiler().compile(
    pipeline_func=forecast_pipeline,
    package_path=pipeline_file,
)

# Configure the Vertex AI Pipelines client
aip.init(
    project="theta-maker-446106-s4",
    location="us-central"  # e.g., "us-central1"
)

# Create and execute the pipeline
job = aip.PipelineJob(
    display_name="kaggle_forecast",
    template_path=pipeline_file,
    parameter_values={
        "file_path": "/home/jupyter/.cache/kagglehub/datasets/sudipmanchare/simulated-sales-data-with-timeseries-features/versions/2/sales.csv",
        "project_id": "theta-maker-446106-s4",
        "dataset_id": 'kaggle',
        "table_id": 'ts_sales',
    }
)
job.submit()
