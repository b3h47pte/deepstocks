#
# Unified format for results coming from various APIs.
#
import datetime
from enum import Enum

class Exchanges(Enum):
    NYSE = 0
    NASDAQ = 1
    OTC = 2
    UNKNOWN = 3

class ExchangeType(Enum):
    EQUITY = 0
    UNKNOWN = 1

class CompanyExData(object):
    def __init__(self, symbol, exchange, exType):
        assert isinstance(symbol, str)
        assert isinstance(exchange, Exchanges)
        assert isinstance(exType, ExchangeType)
        self.symbol = symbol
        self.exchange = exchange
        self.exType = exType

class EquityPriceData(object):
    def __init__(self, dateTime, price, volume):
        assert isinstance(dateTime, datetime.datetime)
        assert isinstance(price, float)
        assert isinstance(volume, int)
        self.dateTime = dateTime
        self.price = price
        self.volume = volume
