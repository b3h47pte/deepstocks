#
# Utilities for reading in information of a company off the database.
#

from .database import Base
from sqlalchemy import Integer, Column, String, ForeignKey
from sqlalchemy.orm import relationship

class Company(Base):
    __tablename__ = 'company'

    name = Column(String, nullable=False)
    symbol = Column(String, nullable=False, unique=True)
    industryId = Column(Integer, ForeignKey('industry.id'))
    industry = relationship('Industry', back_populates='companies')
    equity = relationship('Equity', back_populates='company')
