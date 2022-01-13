
import json
import pytz
from datetime import datetime


def str_map(str1):

    str1 = '{"' + str1\
    .replace("b","")\
    .replace('"', '')\
    .replace("'", '')\
    .replace(",", '","')\
    .replace("=", '":"')\
    .replace("&", '","')\
    .replace("PASSKEY:", 'PASSKEY":"') + '"}'

    convertedDict = json.loads(str1)

    sensorDict = {
        'soilmoisture1' : float(convertedDict['soilmoisture1']),
        'soilatt1' : float(convertedDict['soilatt1']),
        'soilmoisture2' : float(convertedDict['soilmoisture2']),
        'soilatt2' : float(convertedDict['soilatt2']),
        'soilmoisture3' : float(convertedDict['soilmoisture3']),
        'soilatt3' : float(convertedDict['soilatt3'])
    }

    outputDict = {
        'stationtype' : str(convertedDict['stationtype']),
        'sensordateutc' : str(convertedDict['dateutc']),
        'functiondatelocal' : str(datetime.now(pytz.timezone('US/Eastern'))),
        'tempinf' : float(convertedDict['tempinf']),
        'humidityin' : float(convertedDict['humidityin']),
        'aromrelin' : float(convertedDict['aromrelin']),
        'aromasin' : float(convertedDict['aromasin']),
        'freq' : str(convertedDict['freq']),
        'model' : str(convertedDict['model']),
        'soilsensors' : sensorDict
    }
   
    return outputDict