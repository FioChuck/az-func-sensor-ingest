import logging
import json
import azure.functions as func
from .functions.EcoWittPrep import *
import pytz
from datetime import datetime

def main(req: func.HttpRequest, ex_emb: func.Out[func.Document], ex_ref: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

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

    ## Logging only
    # convertedString = json.dumps(output_dict, default=str)
    # logging.info('json string: ' + convertedString)
    ##

    newdocs_emb = ex_emb.DocumentList()

    for item in output_lst_emb:
        newdocs_emb.append(func.Document.from_dict(item))
    ex_emb.set(newdocs_emb)


    newdocs_ref = ex_ref.DocumentList()

    for item in output_lst_ref:
        newdocs_ref.append(func.Document.from_dict(item))
    ex_ref.set(newdocs_ref)

    return 'success'