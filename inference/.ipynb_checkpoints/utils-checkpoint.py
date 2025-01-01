from google.cloud import aiplatform

def get_registered_model(display_name: str, project_id: str, region: str):
    aiplatform.init(project=project_id, location=region)

    # Get the registered model
    models = aiplatform.Model.list(filter=f"display_name={display_name}")
    if not models:
        raise ValueError(f"No model found with display name: {display_name}")
    
    model = models[0]
    print(f"Retrieved model: {model.resource_name}")
    return model
