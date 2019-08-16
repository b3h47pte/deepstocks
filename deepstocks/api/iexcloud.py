#
# Handles dealing with the IEX Cloud API.
#

import datetime
import requests
import deepstocks.api.cache as cache
import deepstocks.config as config
import time

_kSecondsBetweenRequests = 0.01
_lastApiRequestTime = None

def _iexApiLimiter():
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


def iexGetHistoricalStockPrice(symbol):
    _iexApiLimiter()

    from deepstocks.api.unified import EquityPriceData

    params = {
        'token': config.getConfigValue(config.kIEXCloudKey)
    }
    apiUrl = 'https://cloud.iexapis.com/stable/stock/{0}/chart/max'.format(symbol)

    s = requests.Session()
    req = requests.Request('GET', apiUrl, params=params)
    prepReq = req.prepare()

    cacheData = cache.getCachedResponse(prepReq.url)
    if cacheData is None:
        data = s.send(prepReq).json()
    else:
        data = cacheData

    retData = []
    for datum in data:
        equityDatum = EquityPriceData(
            dateTime=datetime.datetime.strptime(datum['date'], '%Y-%m-%d'),
            volume=int(datum['volume']),
            openPrice=float(datum['open']),
            closePrice=float(datum['close']),
            highPrice=float(datum['high']),
            lowPrice=float(datum['low']))
        retData.append(equityDatum)

    cache.storeCachedResponse(prepReq.url, data)
    return retData
