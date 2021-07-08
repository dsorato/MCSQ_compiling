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

    survey_itemid = Column(String, primary_key=True)
    surveyid = Column(String, ForeignKey('survey.surveyid'), nullable=False)
    text = Column(String)
    item_value = Column(String)
    moduleid = Column(Integer, ForeignKey('module.moduleid'))
    requestid = Column(Integer, ForeignKey('request.requestid'))
    responseid = Column(Integer, ForeignKey('response.responseid'))
    instructionid = Column(Integer, ForeignKey('instruction.instructionid'))
    introductionid = Column(Integer, ForeignKey('introduction.introductionid'))
    country_language = Column(String, nullable=False)
    item_is_source = Column(Boolean)
    item_name = Column(String)
    item_type = Column(String)
    pos_tagged_text = Column(String)
    ner_tagged_text = Column(String)

    survey = relationship("Survey", backref=backref("survey_item", uselist=False))
    module = relationship("Module", backref="module")
    request = relationship("Request", backref="request")
    response = relationship("Response", backref="response")
    instruction = relationship("Instruction", backref="instruction")
    introduction = relationship("Introduction", backref="introduction")



    def __init__(self, survey_itemid, surveyid, text, item_value, moduleid, requestid, responseid, instructionid, introductionid, 
        country_language, item_is_source, item_name, item_type, pos_tagged_text, ner_tagged_text):
        
        self.survey_itemid = survey_itemid
        self.surveyid = surveyid
        self.text = text
        self.item_value = item_value
        self.moduleid = moduleid
        self.requestid = requestid
        self.responseid = responseid
        self.instructionid = instructionid
        self.introductionid = introductionid
        self.country_language = country_language
        self.item_is_source = item_is_source
        self.item_name = item_name
        self.item_type = item_type
        self.pos_tagged_text = pos_tagged_text
        self.ner_tagged_text = ner_tagged_text

       

        
        
