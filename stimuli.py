from base import Base
from sqlalchemy import Column, String, Integer, Sequence, ForeignKey

class Stimuli(Base):
    __tablename__ = 'stimuli'

    # emits CREATE SEQUENCE + INTEGER
    stimuliid = Column(Integer, Sequence('stimuli_id_seq'), primary_key=True)
    languagecountry = Column(String)


    def __init__(self, languagecountry):
        self.languagecountry = languagecountry