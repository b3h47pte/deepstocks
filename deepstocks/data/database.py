from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import sessionmaker, scoped_session

@as_declarative()
class Base(object):
    id = Column(Integer, primary_key=True)

_engine = None
_Session = None

def connectToDatabase(dbUrl, scope=None):
    from sqlalchemy import create_engine
    global _engine, _Session
    _engine = create_engine('sqlite:///' + dbUrl)
    _Session = scoped_session(sessionmaker(bind=_engine), scopefunc=scope)
    Base.metadata.create_all(_engine)

def createSession():
    return _Session()

def removeSession():
    _Session.remove()
