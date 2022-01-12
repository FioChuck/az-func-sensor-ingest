import logging
import json
import azure.functions as func
from .functions.EcoWittPrep import *

def main(req: func.HttpRequest, doc: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    input_str = str(req.get_body())
    logging.info('http body: ' + input_str)

    test =  str_map(input_str)
    
    ## Logging only
    convertedString = json.dumps(test)
    logging.info('json string: ' + convertedString)

    newdocs = func.DocumentList() 

    newdocs.append(func.Document.from_dict(test))
    doc.set(newdocs)

    return 'success'