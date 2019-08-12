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

def getHistoricalStockPrice(symbol, startDate=None, endDate=None):
    pass
