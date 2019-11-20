from DB.base import Base
from sqlalchemy import Column, String, Boolean, Integer, Sequence, ForeignKey

class Survey(Base):
    __tablename__ = 'survey'

    surveyid = Column(String, primary_key=True)
    study = Column(String, nullable=False)
    wave_round = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    country_language = Column(String, nullable=False)

    def __init__(self, surveyid, study, wave_round, year, country_language):
        self.surveyid = surveyid
        self.study = study
        self.wave_round = wave_round
        self.year = year
        self.country_language = country_language