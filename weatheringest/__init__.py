import logging
import requests
import json
import os
import azure.functions as func


def main(mytimer: func.TimerRequest, city: func.Out[func.Document], dt: func.Out[func.Document], description: func.Out[func.Document], outputblob: func.Out[bytes]) -> None:


    url1 = 'http://api.openweathermap.org/data/2.5/weather?id=4180439&appid=' + os.environ['weatherApiKey'] # atlanta
    url2 = 'http://api.openweathermap.org/data/2.5/weather?id=4221552&appid=' + os.environ['weatherApiKey'] # savannah

    payload = ""
    headers = {}

    response1 = requests.request("GET", url1, headers=headers, data=payload) # atlanta id
    response2 = requests.request("GET", url2, headers=headers, data=payload) # savannah id

## atlanta ##
    dict1 = response1.json()
    weather = dict1['weather'][0]
    del dict1['id'] # remove id - interferes with cosmos db id
    del dict1['name'] # remove name - replace with city
    del dict1['weather']

    dict1['location'] = {
    'state': 'Georgia',
    'city': 'Atlanta'}

    dict1['weather'] = weather
####

## savannah ##
    dict2 = response2.json()
    weather = dict2['weather'][0]
    del dict2['id'] # remove id - interferes with cosmos db id
    del dict2['name'] # remove name - replace with city
    del dict2['weather']

    dict2['location'] = {
    'state': 'Georgia',
    'city': 'Savannah'}

    dict2['weather'] = weather
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

    city.set(newdocs) # save newdocs to city container
    dt.set(newdocs) # save newdocs to dt container
    description.set(newdocs)

#### Save to ADLS
    # output_json = json.dumps(dict1)
    # outputblob.set(output_json)