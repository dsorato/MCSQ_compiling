"""
MCSQ Alignment table
Author: Danielly Sorato 
Author contact: danielly.sorato@gmail.com
"""

from DB.base import Base
from sqlalchemy import Column, String, Boolean, Integer, Sequence, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy import ForeignKeyConstraint

class Alignment(Base):
    __tablename__ = 'alignment'

    # emits CREATE SEQUENCE + INTEGER
    alignmentid = Column(Integer, Sequence('alignment_id_seq'), primary_key=True)
    source_survey_itemid = Column(String, ForeignKey('survey_item.survey_itemid'))
    target_survey_itemid = Column(String, ForeignKey('survey_item.survey_itemid'))
    source_survey_item_elementid = Column(Integer, ForeignKey('survey_item.survey_item_elementid'))
    target_survey_item_elementid = Column(Integer, ForeignKey('survey_item.survey_item_elementid'))

   	survey_item = relationship("Survey_item", backref="survey_item")
   

    def __init__(self, source_survey_itemid, target_survey_itemid):
        self.source_survey_itemid = source_survey_itemid
        self.target_survey_itemid = target_survey_itemid
        self.source_survey_item_elementid = source_survey_item_elementid
        self.target_survey_item_elementid = target_survey_item_elementid
