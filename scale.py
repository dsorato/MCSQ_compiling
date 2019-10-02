from base import Base
from sqlalchemy import Column, String, Integer, Sequence, ForeignKey

class Scale(Base):
    __tablename__ = 'scale'

    # emits CREATE SEQUENCE + INTEGER
    scaleid = Column(Integer, Sequence('scale_id_seq'), primary_key=True)
    surveyid = Column(Integer, ForeignKey('survey.surveyid'))
    languagecountry = Column(String)


    def __init__(self, surveyid, languagecountry):
        self.surveyid = surveyid
        self.languagecountry = languagecountry