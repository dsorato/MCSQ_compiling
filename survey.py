from base import Base

class Survey(Base):
    __tablename__ = 'survey'

    # emits CREATE SEQUENCE + INTEGER
    surveyid = Column(Integer, Sequence('survey_id_seq'), primary_key=True)
    study = Column(String)
    waveorround = Column(Integer)
    year = Column(Integer)
    surveymode = Column(String)

    def __init__(self, study, waveorround, year, surveymode):
        self.study = study
        self.waveorround = waveorround
        self.year = year
        self.surveymode = surveymode
