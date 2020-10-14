"""
MCSQ Alignment table
Author: Danielly Sorato 
Author contact: danielly.sorato@gmail.com
"""

from DB.base import Base
from sqlalchemy import Column, String, Boolean, Integer, Sequence, ForeignKey
from sqlalchemy.orm import relationship, backref

class Alignment(Base):
    __tablename__ = 'alignment'

    # emits CREATE SEQUENCE + INTEGER
    alignmentid = Column(Integer, Sequence('alignment_id_seq'), primary_key=True)
    source_text = Column(String)
    target_text = Column(String)
    source_survey_itemid = Column(String)
    target_survey_itemid = Column(String)

   

    def __init__(self,source_text, target_text, source_survey_itemid,target_survey_itemid):
        self.source_text = source_text
        self.target_text = target_text
        self.source_survey_itemid = source_survey_itemid
        self.target_survey_itemid = target_survey_itemid
