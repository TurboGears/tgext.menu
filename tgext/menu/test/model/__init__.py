#from sqlalchemy.types import *
from sqlalchemy import *
from sqlalchemy.orm import relation, backref, synonym
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base, synonym_for


from zope.sqlalchemy import ZopeTransactionExtension
from sqlalchemy.orm import scoped_session, sessionmaker

# Global session manager.  DBSession() returns the session object
# appropriate for the current web request.
maker = sessionmaker(autoflush=True, autocommit=False,
                     extension=ZopeTransactionExtension())
DBSession = scoped_session(maker)

DeclarativeBase = declarative_base()

metadata = DeclarativeBase.metadata

class Dictionary(DeclarativeBase):
    __tablename__ = 'dictionary'
    word_id = Column(Integer, primary_key=True)
    word = Column(String(32))

def init_model(engine):
    DBSession.configure(bind=engine)
    
from auth import User, Group, Permission
