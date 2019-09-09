from base import Base
from sqlalchemy import Column, String, Boolean, Integer, Sequence, ForeignKey


class Document(Base):
    __tablename__ = 'document'

    documentid = Column(String, primary_key=True)
    moduleid = Column(Integer, ForeignKey('module.moduleid'))
    surveyid = Column(Integer, ForeignKey('survey.surveyid'))
    sourcecountrylanguage = Column(String)
    countrylanguage = Column(String)
    documentistranslation = Column(Boolean)
    module = relationship("Module", backref=backref("document", uselist=False))
    survey = relationship("Survey", backref="document")

    def __init__(self, documentid, countrylanguage):
        self.documentid = documentid
        self.countrylanguage = countrylanguage
        self.sourcecountrylanguage = sourcecountrylanguage
        self.countrylanguage = countrylanguage
        self.documentistranslation = documentistranslation
