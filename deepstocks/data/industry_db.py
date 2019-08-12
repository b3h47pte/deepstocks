#
# Utilities for reading in information of an industry off the database.
#

from .database import Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

class Industry(Base):
    __tablename__ = 'industry'

    name = Column(String, nullable=False, unique=True)
    companies = relationship('Company', back_populates='industry')
