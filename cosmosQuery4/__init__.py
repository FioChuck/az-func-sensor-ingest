import datetime
import logging
from azure.cosmos import exceptions, CosmosClient, PartitionKey
import os
import json
import azure.functions as func
import pandas as pd

logger = logging.getLogger("azure.core.pipeline.policies.http_logging_policy")
logger.setLevel(logging.WARNING)

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()


    logging.info('Python timer trigger function ran at %s', utc_timestamp)

    client = CosmosClient(os.environ['cosmosEndPoint'], os.environ['cosmosKey'])

    database = client.get_database_client('telemetry')
    container = database.get_container_client('openweathermap-description')

    out = container.query_items(query = 'SELECT * FROM c WHERE c.weather.description = "overcast clouds"',populate_query_metrics = True, enable_cross_partition_query = True)
    
    dflist = []
    for item in out:
        dflist.append(dict(item))
        
    df = pd.DataFrame(dflist)

    logging.info('Weather Query Result Count: ' + str(df.shape) )

    ########### second query
    container = database.get_container_client('climate_ref')

    out = container.query_items(query = 'SELECT * FROM c WHERE c.doctype = "sensor"',populate_query_metrics = True, enable_cross_partition_query = True)
    
    dflist = []
    for item in out:
        dflist.append(dict(item))
        
    df = pd.DataFrame(dflist)

    logging.info('IoT Query1 Result Count: ' + str(df.shape) )

    logging.info('Complete')
    
    ########### third query
    container = database.get_container_client('climate_emb')

    out = container.query_items(query = 'SELECT * FROM c WHERE c.tempinf > 70',populate_query_metrics = True, enable_cross_partition_query = True)
    
    dflist = []
    for item in out:
        dflist.append(dict(item))
        
    df = pd.DataFrame(dflist)

    logging.info('IoT Query2 Result Count: ' + str(df.shape) )

    logging.info('Complete')