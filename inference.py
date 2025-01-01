from prophet import Prophet
from utils import *
import pandas as pd
import logging

def predict(display_name:str, project_id:str, region:str)-> pd.DataFrame:
    
    logging.info('inference started')
    model = get_registered_model(display_name, project_id, region)
    future = model.make_future_dataframe(periods=365)
    forecast = model.predict(future)
    forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    logging.info('inference completed')
    
    return forecast
