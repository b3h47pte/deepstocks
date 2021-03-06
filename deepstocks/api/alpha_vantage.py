#
# Handles dealing with the Alpha Vantaga API.
#

import datetime
import requests
import deepstocks.api.cache as cache
import deepstocks.config as config
import time

_kSecondsBetweenRequests = 2
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
        'symbol': symbol.replace('.',''),
        'outputsize': 'full',
        'datatype': 'json',
        'apikey': config.getConfigValue(config.kAlphaVantageConfigKey),
    }
    apiUrl = 'https://www.alphavantage.co/query'

    s = requests.Session()
    headers = requests.utils.default_headers()
    headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'
    req = requests.Request('GET', apiUrl, params=params, headers=headers)
    prepReq = req.prepare()

    cacheData = cache.getCachedResponse(prepReq.url)
    if cacheData is None:
        data = s.send(prepReq).json()
    else:
        data = cacheData

    retData = []
    timeData = data['Time Series (Daily)']
    for dateTime, priceDatum in timeData.items():
        equityDatum = EquityPriceData(
            dateTime=datetime.datetime.strptime(dateTime, '%Y-%m-%d'),
            volume=int(priceDatum['5. volume']),
            openPrice=float(priceDatum['1. open']),
            closePrice=float(priceDatum['4. close']),
            highPrice=float(priceDatum['2. high']),
            lowPrice=float(priceDatum['3. low']))
        retData.append(equityDatum)

    cache.storeCachedResponse(prepReq.url, data)
    return retData
