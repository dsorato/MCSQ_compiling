"""
MCSQ survey_item table
Author: Danielly Sorato 
Author contact: danielly.sorato@gmail.com
"""

from DB.base import Base
from sqlalchemy import Column, String, Boolean, Integer, Sequence, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship, backref


class Survey_item(Base):
    __tablename__ = 'survey_item'

    # emits CREATE SEQUENCE + INTEGER
    survey_item_elementid = Column(Integer, Sequence('survey_item_element_id_seq'), primary_key=True)
    survey_itemid = Column(String, primary_key=True)
    surveyid = Column(String, ForeignKey('survey.surveyid'), nullable=False)
    moduleid = Column(Integer, ForeignKey('module.moduleid'))
    requestid = Column(Integer, ForeignKey('request.requestid'))
    responseid = Column(Integer)
    response_item_id = Column(Integer)
    instructionid = Column(Integer, ForeignKey('instruction.instructionid'))
    introductionid = Column(Integer, ForeignKey('introduction.introductionid'))
    country_language = Column(String, nullable=False)
    item_is_source = Column(Boolean)
    item_name = Column(String)
    item_type = Column(String)
    ForeignKeyConstraint(['responseid', 'response_item_id'], ['response.responseid','response.response_item_id'])


    survey = relationship("Survey", backref=backref("survey_item", uselist=False))
    module = relationship("Module", backref="module")
    request = relationship("Request", backref="request")
    instruction = relationship("Instruction", backref="instruction")
    introduction = relationship("Introduction", backref="introduction")



    def __init__(self, survey_itemid, surveyid, moduleid, requestid, responseid, response_item_id, instructionid,introductionid, country_language, item_is_source, item_name, item_type):
        self.survey_itemid = survey_itemid
        self.surveyid = surveyid
        self.moduleid = moduleid
        self.requestid = requestid
        self.responseid = responseid
        self.response_item_id = response_item_id
        self.instructionid = instructionid
        self.introductionid = introductionid
        self.country_language = country_language
        self.item_is_source = item_is_source
        self.item_name = item_name
        self.item_type = item_type

       

        
        
