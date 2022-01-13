import logging
import json
import azure.functions as func
from .functions.EcoWittPrep import *

def main(req: func.HttpRequest, doc: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    input_str = str(req.get_body())
    logging.info('http body: ' + input_str)

    output_dict =  str_map(input_str)

    ## Logging only
    convertedString = json.dumps(output_dict, default=str)
    logging.info('json string: ' + convertedString)

    newdocs = func.DocumentList() 

    newdocs.append(func.Document.from_dict(output_dict))

    print(newdocs.data)

    doc.set(newdocs)

    return 'success'