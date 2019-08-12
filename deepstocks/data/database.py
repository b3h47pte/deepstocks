from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import sessionmaker

@as_declarative()
class Base(object):
    id = Column(Integer, primary_key=True)

_engine = None
_Session = None

def connectToDatabase(dbUrl):
    from sqlalchemy import create_engine
    global _engine, _Session
    _engine = create_engine('sqlite:///' + dbUrl)
    _Session = sessionmaker(bind=_engine)
    Base.metadata.create_all(_engine)

def createSession():
    return _Session()
