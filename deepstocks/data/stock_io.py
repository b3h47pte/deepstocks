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

def getHistoricalStockPrice(symbol, local=False, session=None):
    from deepstocks.api.alpha_vantage import avGetHistoricalStockPrice
    from deepstocks.api.iexcloud import iexGetHistoricalStockPrice
    from deepstocks.api.unified import EquityPriceData

    if not local:
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
    else:
        assert(session is not None)
        from deepstocks.data import Equity, Company
        results = session.query(Equity).join(Equity.company).filter(Company.symbol == symbol).order_by(Equity.dateTime.asc()).all()
        return [EquityPriceData(
            dateTime=s.dateTime,
            volume=s.volume,
            openPrice=s.openPrice,
            closePrice=s.closePrice,
            highPrice=s.highPrice,
            lowPrice=s.lowPrice)
            for s in results]
