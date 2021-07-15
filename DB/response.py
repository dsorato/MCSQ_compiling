"""
MCSQ Response table
Author: Danielly Sorato 
Author contact: danielly.sorato@gmail.com
"""

from DB.base import Base
from sqlalchemy import Column, String, Boolean, Integer, Sequence, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy import ForeignKeyConstraint

class Response(Base):
    __tablename__ = 'response'

    # emits CREATE SEQUENCE + INTEGER
    responseid = Column(Integer, Sequence('response_id_seq'), primary_key=True)
    text = Column(String)
    item_value = Column(String)
    pos_tagged_text = Column(String)
    ner_tagged_text = Column(String)
   
    def __init__(self, text, item_value, pos_tagged_text, ner_tagged_text):
        self.text = text
        self.item_value = item_value
        self.pos_tagged_text = pos_tagged_text
        self.ner_tagged_text = ner_tagged_text