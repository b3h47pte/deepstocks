#
# Utilities for reading in information of technical indicators off the database.
#

from .database import Base
from .stock_db import Equity
from sqlalchemy import Column, DateTime, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

class TechnicalIndicatorMixin(object):
    dateTime = Column(DateTime, nullable=False)

def createTechnicalIndicator(clsName, strName, columns):
    fullAttributes = columns
    fullAttributes['__tablename__'] = strName
    fullAttributes['equityId'] = Column(Integer, ForeignKey(Equity.id), nullable=False)
    fullAttributes['equity'] = relationship('Equity', back_populates=strName)

    return type(clsName, (TechnicalIndicatorMixin, Base,), fullAttributes)

RSITechIndicator = createTechnicalIndicator('RSITechIndicator', 'rsi', {
    'period': Column(Integer, nullable=False),
    'value': Column(Float, nullable=False)
})
