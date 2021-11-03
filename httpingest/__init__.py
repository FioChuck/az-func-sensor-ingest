import logging
import json
import azure.functions as func


def main(req: func.HttpRequest, outputblob: func.Out[bytes]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    var1 = req.get_json
    logging.info(var1)

# test commit
    # try:
    #     req_body = req.get_json()
    # except ValueError:
    #     logging.info('Error reading input json')
    #     pass

    input_dict = var1

    output_json = json.dumps(input_dict)
    outputblob.set(output_json)

    return "success"