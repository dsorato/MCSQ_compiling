from DB.base import Base
from sqlalchemy import Column, String, Boolean, Integer, Sequence, ForeignKey
from sqlalchemy.orm import relationship, backref


class Survey_item(Base):
    __tablename__ = 'survey_item'

    survey_itemid = Column(String, primary_key=True)
    surveyid = Column(String, ForeignKey('survey.surveyid'), nullable=False)
    moduleid = Column(Integer, ForeignKey('module.moduleid'))
    country_language = Column(String, nullable=False)
    item_is_source = Column(Boolean)
    item_name = Column(String)
    item_type = Column(String)


    survey = relationship("Survey", backref=backref("survey_item", uselist=False))
    module = relationship("Module", backref="survey_item")



    def __init__(self, survey_itemid, surveyid, moduleid, country_language, item_is_source, item_name, item_type):
        self.survey_itemid = survey_itemid
        self.surveyid = surveyid
        self.moduleid = moduleid
        self.country_language = country_language
        self.item_is_source = item_is_source
        self.item_name = item_name
        self.item_type = item_type

       

        
        
