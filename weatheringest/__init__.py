import logging
import requests
import json
import os
import azure.functions as func


def main(mytimer: func.TimerRequest, doc: func.Out[func.Document]) -> None:

    if mytimer.past_due:
        logging.info('The timer is past due!')


    url1 = 'http://api.openweathermap.org/data/2.5/weather?id=4180439&appid=' + os.environ['weatherApiKey'] # atlanta
    url2 = 'http://api.openweathermap.org/data/2.5/weather?id=4221552&appid=' + os.environ['weatherApiKey'] # savannah

    payload = ""
    headers = {}

    response1 = requests.request("GET", url1, headers=headers, data=payload) # atlanta id
    response2 = requests.request("GET", url2, headers=headers, data=payload) # savannah id

## atlanta ##
    dict1 = response1.json()
    del dict1['id'] # remove id - interferes with cosmos db id
    del dict1['name'] # remove name - replace with city

    dict1['location'] = {
    'state': 'Georgia',
    'city': 'Atlanta'}
####

## savannah ##
    dict2 = response2.json()
    del dict2['id'] # remove id - interferes with cosmos db id
    del dict2['name'] # remove name - replace with city

    dict2['location'] = {
    'state': 'Georgia',
    'city': 'Savannah'}
####

## for logging only
    convertedString1 = json.dumps(response1.json())
    logging.info('json string1: ' + convertedString1)

    convertedString2 = json.dumps(response2.json())
    logging.info('json string2: ' + convertedString2)
####

    newdocs = func.DocumentList() 
    newdocs.append(func.Document.from_dict(dict1))
    newdocs.append(func.Document.from_dict(dict2))
    doc.set(newdocs)