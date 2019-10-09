from base import Base
from sqlalchemy import Column, String, Boolean, Integer, Sequence, ForeignKey
from sqlalchemy.orm import relationship, backref


class Document(Base):
    __tablename__ = 'document'

    documentid = Column(String, primary_key=True)
    surveyid = Column(Integer, ForeignKey('survey.surveyid'))
    moduleid = Column(Integer, ForeignKey('module.moduleid'))
    scaleid = Column(Integer, ForeignKey('scale.scaleid'))
    stimuliid = Column(Integer, ForeignKey('stimuli.stimuliid'))
    sourcedocumentid = Column(String)
    sourcecountrylanguage = Column(String)
    countrylanguage = Column(String)
    documentistranslation = Column(Boolean)
    module = relationship("Module", backref=backref("document", uselist=False))
    scale = relationship("Scale", backref=backref("document", uselist=False))
    stimuli = relationship("Stimuli", backref=backref("document", uselist=False))
    survey = relationship("Survey", backref="document")

    def __init__(self, documentid, surveyid, scaleid, stimuliid, moduleid, sourcedocumentid, sourcecountrylanguage, countrylanguage, documentistranslation):
        self.documentid = documentid
        self.surveyid = surveyid
        self.scaleid = scaleid
        self.stimuliid = stimuliid
        self.moduleid = moduleid
        self.sourcedocumentid = sourcedocumentid
        self.sourcecountrylanguage = sourcecountrylanguage
        self.countrylanguage = countrylanguage
        self.documentistranslation = documentistranslation
        
