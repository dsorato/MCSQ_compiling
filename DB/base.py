from sqlalchemy.orm import *
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import DB.credentials as creds

engine = create_engine("postgres://"+creds.PGUSER+":"+creds.PGPASSWORD+"@"+ creds.PGHOST +":5432/"+creds.PGDATABASE)
# use session_factory() to get a new Session
_SessionFactory = sessionmaker(bind=engine)

Base = declarative_base()

#Factory that encapsulates creation of sessions
def session_factory():
    Base.metadata.create_all(engine)
    return _SessionFactory()
