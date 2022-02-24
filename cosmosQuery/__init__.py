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

    for x in range(100):
        out = container.query_items(query = 'SELECT * FROM c WHERE c.weather.description = "clear sky"',populate_query_metrics = True, enable_cross_partition_query = True)
        dflist = []
        for item in out:
            dflist.append(dict(item))
            
        df = pd.DataFrame(dflist)
        logging.info('Query Number' + str(x) )
        logging.info('Query Result Count: ' + str(df.shape) )
    