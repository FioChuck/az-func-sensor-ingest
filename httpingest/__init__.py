import logging
import json
import datetime as dt
import azure.functions as func
import pandas as pd

def main(req: func.HttpRequest, doc: func.Out[bytes]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    logging.info('http body: ' + str(req.get_body()))

    ## convert input string to output string
    ## intermedieate dictionary created

    input_str = '{"' + str(req.get_body())\
    .replace("b","")\
    .replace('"', '')\
    .replace("'", '')\
    .replace(",", '","')\
    .replace("=", '":"')\
    .replace("&", '","')\
    .replace("PASSKEY:", 'PASSKEY":"') + '"}'

    logging.info('output string: ' + input_str)

    input_json = json.loads(input_str)

## Save to Cosmos DB
    newdocs = func.DocumentList()
    newproduct_dict = {
        "id": "stuff1",
        "name": "stuff2"
    }
    
    logging.info('output dict: ' + str(newproduct_dict))

    newdocs.append(func.Document.from_dict(newproduct_dict))
    doc.set(newdocs)

   ## Save to Cosmos DB END 

    df = pd.json_normalize(input_json) # convert input json to pandas dataframe
    df = df.reset_index(drop = True) # remove index column
    df["ingest_time"] = dt.datetime.now() # add datetime

    output_str = df.to_csv(index=False) # convert pandas dataframe to string
    ## output string saved to outputblob binding (see function.json)

    logging.info('output string: ' + output_str)


    ## save output string to adls 
    # outputblob.set(output_str)

    logging.info('job complete')

    return "success"