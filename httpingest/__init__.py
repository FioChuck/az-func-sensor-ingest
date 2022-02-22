import logging
import azure.functions as func
from .functions.EcoWittPrep import *
import pytz
from datetime import datetime
import os

   
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey

def main(req: func.HttpRequest) -> func.HttpResponse:
    # , ex_emb: func.Out[func.Document], ex_ref: func.Out[func.Document]
    logging.info('Python HTTP trigger function processed a request.')

    input_str = str(req.get_body())

    def create_items(container,item):
        client = cosmos_client(os.environ['cosmosEndPoint'], os.environ['cosmosKey'])

        database = client.get_database_client('telemetry')

        # container = database.get_container_client('climate_ref')
        container = database.get_container_client('climate_ref')

        container.create_item(body=item)

    logging.info('http body: ' + input_str) # log message recieved

    processingtime = str(datetime.now(pytz.timezone('US/Eastern'))) # declare processing time

    output_lst_emb = [] # list of output something
    output_lst_ref = [] # list of output something

    station_doc = str_map_emb(input_str, processingtime) # calculate embedded docs
    station_doc_ref, sensor_doc1, sensor_doc2, sensor_doc3 = str_map_ref(input_str, processingtime)

    output_lst_emb.append(station_doc)

    output_lst_ref.append(station_doc_ref)
    output_lst_ref.append(sensor_doc1)
    output_lst_ref.append(sensor_doc2)
    output_lst_ref.append(sensor_doc3)

    ## Logging only
    # convertedString = json.dumps(output_dict, default=str)
    # logging.info('json string: ' + convertedString)
    ##

    # for item in output_lst_emb:
        # newdocs_emb.append(func.Document.from_dict(item))


    for item in output_lst_ref:
        create_items('climate_ref',item)


    return 'success'