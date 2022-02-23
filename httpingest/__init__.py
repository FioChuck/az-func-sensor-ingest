import logging
import azure.functions as func
from .functions.EcoWittPrep import *
from .functions.Cosmos import *
import pytz
from datetime import datetime


def main(req: func.HttpRequest) -> func.HttpResponse:

    input_str = str(req.get_body())

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

    try:
        for item in output_lst_ref:
            create_items('climate_ref',item)
            logging.info('Success Writing to Cosmos: ' + item['id'])
    except:
        logging.info('Error Writing to Cosmos: ' + item['id'])

    try:
        for item in output_lst_emb:
            create_items('climate_emb',item)
            logging.info('Success Writing to Cosmos: ' + item['id'])
    except:
        logging.info('Error Writing to Cosmos: ' + item['id'])

    return 'success'