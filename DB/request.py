"""
MCSQ Request table
Author: Danielly Sorato 
Author contact: danielly.sorato@gmail.com
"""

from DB.base import Base
from sqlalchemy import Column, String, Boolean, Integer, Sequence, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy import ForeignKeyConstraint

class Request(Base):
    __tablename__ = 'request'

    # emits CREATE SEQUENCE + INTEGER
    requestid = Column(Integer, Sequence('request_id_seq'), primary_key=True)
    text = Column(String)
    pos_tagged_text = Column(String)
    ner_tagged_text = Column(String)
   

    def __init__(self, text, pos_tagged_text, ner_tagged_text):
        self.text = text
        self.pos_tagged_text = pos_tagged_text
        self.ner_tagged_text = ner_tagged_text