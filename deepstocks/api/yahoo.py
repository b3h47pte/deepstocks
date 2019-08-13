#
# Handles dealing with Yahoo finance API.
# 
import requests
import string

def yahooGetSymbolsFromCompanyName(companyName):
    from deepstocks.api.unified import Exchanges, ExchangeType, CompanyExData

    # Split to get words to try to automatically clean up the company name so that we can
    # find the stock symbol on Yahoo. Works OK. Not that great though.
    ignoreWords = set(['the'])
    breakWords = set(['corp', 'inc', 'holding', 'company', 'ltd', 'plc', 'limited'])
    strictBreakWords = set(['&'])
    splitSpacesName = []
    for s in companyName.split():
        cleanS = s.rstrip(' ,')

        ignoreFlag = False
        for word in ignoreWords:
            if word == cleanS.lower():
                ignoreFlag = True
                break

        if ignoreFlag:
            continue

        breakFlag = False
        for word in breakWords:
            if word in cleanS.lower():
                breakFlag = True
                break

        if breakFlag:
            break

        breakFlag = False
        for word in strictBreakWords:
            if word == cleanS.lower():
                breakFlag = True
                break

        if breakFlag:
            break

        splitSpacesName.append(cleanS)
        if cleanS != s:
            break

    queryCompanyName = ' '.join(splitSpacesName).strip()
    params = {
        'query': queryCompanyName,
        'region': 'US',
        'lang': 'en',
    }
    apiUrl = 'http://autoc.finance.yahoo.com/autoc'
    r = requests.get(apiUrl, params=params)
    data = r.json()

    def exchDispToExchanges(d):
        if d == 'NYSE':
            return Exchanges.NYSE
        elif d == 'NASDAQ':
            return Exchanges.NASDAQ
        elif d == 'OTC Markets' or d == 'OTC BB':
            return Exchanges.OTC
        return Exchanges.UNKNOWN

    def typeToExchangeType(t):
        if t == 'S':
            return ExchangeType.EQUITY
        return ExchangeType.UNKNOWN

    retData = []
    try:
        for datum in data['ResultSet']['Result']:
            exData = CompanyExData(
                symbol=datum['symbol'],
                exchange=exchDispToExchanges(datum['exchDisp']),
                exType=typeToExchangeType(datum['type']))
            retData.append(exData)
    except:
        print('Invalid query: ', r.url)
    return retData
