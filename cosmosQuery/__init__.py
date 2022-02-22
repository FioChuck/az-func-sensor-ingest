import datetime
import logging
from azure.cosmos import exceptions, CosmosClient, PartitionKey
import os
import json
import azure.functions as func
import pandas as pd

print('test')

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    dflist = []


    logging.info('Python timer trigger function ran at %s', utc_timestamp)

    client = CosmosClient(os.environ['cosmosEndPoint'], os.environ['cosmosKey'])

    database = client.get_database_client('telemetry')
    container = database.get_container_client('climate')
    # out = container.query_items(query='SELECT * FROM c',enable_cross_partition_query=True,populate_query_metrics: Optional[bool] = None)

    out = container.query_items(query = 'SELECT * FROM c',populate_query_metrics = True, enable_cross_partition_query = True)

    # query_items(query: str, parameters: Optional[List[Dict[str, object]]] = None, partition_key: Optional[Any] = None, enable_cross_partition_query: Optional[bool] = None, max_item_count: Optional[int] = None, enable_scan_in_query: Optional[bool] = None, populate_query_metrics: Optional[bool] = None, **kwargs: Any) -> Iterable[Dict[str, Any]]
    
    for item in out:
        dflist.append(dict(item))
        
    df = pd.DataFrame(dflist)


    df.head()

