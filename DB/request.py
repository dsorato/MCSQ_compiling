from DB.base import Base
from sqlalchemy import Column, String, Boolean, Integer, Sequence, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy import ForeignKeyConstraint

class Request(Base):
    __tablename__ = 'request'

    # emits CREATE SEQUENCE + INTEGER
    requestid = Column(Integer, Sequence('request_id_seq'), primary_key=True)
    text = Column(String)


    def __init__(self, text):
        self.text = text