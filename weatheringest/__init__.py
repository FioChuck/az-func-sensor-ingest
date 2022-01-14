import logging
import requests
import json
import os
import azure.functions as func


def main(mytimer: func.TimerRequest, doc: func.Out[func.Document]) -> None:

    if mytimer.past_due:
        logging.info('The timer is past due!')


    url = 'http://api.openweathermap.org/data/2.5/weather?id=' + os.environ['weatherApiKey']

    payload = ""
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    dict1 = response.json()
    del dict1['id']

    convertedString = json.dumps(response.json())
    logging.info('json string: ' + convertedString)


    newdocs = func.DocumentList() 

    newdocs.append(func.Document.from_dict(dict1))

    print(newdocs.data)

    doc.set(newdocs)