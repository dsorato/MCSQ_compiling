from DB.base import Base
from sqlalchemy import Column, String, Boolean, Integer, Sequence, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy import ForeignKeyConstraint

class Response(Base):
    __tablename__ = 'response'

    # emits CREATE SEQUENCE + INTEGER
    responseid = Column(Integer, primary_key=True)
    response_item_id = Column(Integer, Sequence('response_item_id_seq'), primary_key=True)
    text = Column(String)
    item_value = Column(String)


    def __init__(self, responseid, text, item_value):
    	self.responseid = responseid
    	self.text = text
    	self.item_value = item_value