#
# Handles dealing with the Alpha Vantaga API.
#

import datetime
import requests
import deepstocks.config as config
import time

_kSecondsBetweenRequests = 60
_lastApiRequestTime = None

def _avApiLimiter():
    global _kSecondsBetweenRequests
    global _lastApiRequestTime

    reqTime = datetime.datetime.now()
    if _lastApiRequestTime is None:
        _lastApiRequestTime = reqTime
        return

    elapsedSeconds = (reqTime - _lastApiRequestTime).total_seconds()
    if elapsedSeconds >= _kSecondsBetweenRequests:
        _lastApiRequestTime = reqTime
        return

    time.sleep(_kSecondsBetweenRequests - elapsedSeconds)
    _lastApiRequestTime = reqTime

def avGetHistoricalStockPrice(symbol):
    _avApiLimiter()

    from deepstocks.api.unified import EquityPriceData

    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol,
        'outputsize': 'full',
        'datatype': 'json',
        'apikey': config.getConfigValue(config.kAlphaVantageConfigKey),
    }
    apiUrl = 'https://www.alphavantage.co/query'
    r = requests.get(apiUrl, params=params)
    data = r.json()

    retData = []
    timeData = data['Time Series (Daily)']
    for dateTime, priceDatum in timeData.items():
        equityDatum = EquityPriceData(
            dateTime=datetime.datetime.strptime(dateTime, '%Y-%m-%d'),
            price=float(priceDatum['4. close']),
            volume=int(priceDatum['5. volume']))
        retData.append(equityDatum)
    return retData
