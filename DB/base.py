from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import DB.credentials as creds

engine = create_engine("postgres://"+creds.PGUSER+":"+creds.PGPASSWORD+"@"+ creds.PGHOST +":5432/"+creds.PGDATABASE)
#engine = create_engine("postgres://postgres:upf@localhost:5432/PCSQ")
# use session_factory() to get a new Session
_SessionFactory = sessionmaker(bind=engine)

Base = declarative_base()


def session_factory():
    Base.metadata.create_all(engine)
    return _SessionFactory()