import logging
import json
import azure.functions as func
import ast

def main(req: func.HttpRequest, outputblob: func.Out[bytes]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    logging.info('http body: ' + str(req.get_body()))

    var1 = '{"' + str(req.get_body())\
    .replace("b","")\
    .replace('"', '')\
    .replace("'", '')\
    .replace(",", '","')\
    .replace("=", '":"')\
    .replace("&", '","')\
    .replace("PASSKEY:", 'PASSKEY":"') + '"}'

    convertedDict = json.loads(var1)

    convertedString = json.dumps(convertedDict)
    logging.info('json string: ' + convertedString)

    outputblob.set(convertedString)
    logging.info('job complete')

    return "success"