#
# Utilities for reading in information of stocks off the database.
#

from .database import Base
from sqlalchemy import Column, DateTime, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

class Equity(Base):
    __tablename__ = 'equity'

    dateTime = Column(DateTime, nullable=False)
    companyId = Column(Integer, ForeignKey('company.id'), nullable=False)
    company = relationship('Company', back_populates='equity')

    volume = Column(Integer, nullable=False)
    openPrice = Column(Float, nullable=False)
    closePrice = Column(Float, nullable=False)
    highPrice = Column(Float, nullable=False)
    lowPrice = Column(Float, nullable=False)
