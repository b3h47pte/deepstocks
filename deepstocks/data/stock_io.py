#
# Utilities for obtaining stock information and reading/write stock information.
#
import datetime

def getSymbolFromCompanyName(companyName):
    from deepstocks.api.yahoo import yahooGetSymbolsFromCompanyName
    from deepstocks.api.unified import Exchanges, ExchangeType
    symbols = yahooGetSymbolsFromCompanyName(companyName)

    # Filter out symbols that aren't NYSE/NASDAQ and aren't equity.
    filteredSymbols = [s for s in symbols if (s.exchange != Exchanges.UNKNOWN and s.exType != ExchangeType.UNKNOWN)]

    # If more than one still exists, pick the first.
    if not filteredSymbols:
        return None
    return filteredSymbols[0].symbol

def getHistoricalStockPrice(symbol):
    from deepstocks.api.alpha_vantage import avGetHistoricalStockPrice
    from deepstocks.api.iexcloud import iexGetHistoricalStockPrice

    try:
        print('......Retrieving from AlphaVantage')
        return avGetHistoricalStockPrice(symbol)
    except Exception as ex:
        print('......Failed to retrieve from AlphaVantage: {0}'.format(ex))
        try:
            print('......Retrieving from IEX')
            return iexGetHistoricalStockPrice(symbol)
        except Exception as ex:
            print('......Failed to retrieve from IEX: {0}'.format(ex))
            raise Exception('Failed to retrieve historical stock price for {0}'.format(symbol))
