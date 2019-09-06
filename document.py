from base import Base


class Document(Base):
    __tablename__ = 'document'

    documentid = Column(String, primary_key=True)
    moduleid = Column(Integer, ForeignKey('module.moduleid'))
    surveyid = Column(Integer, ForeignKey('survey.surveyid'))
    countrylanguage = Column(String)
    module = relationship("Module", backref=backref("document", uselist=False))
    actor = relationship("Survey", backref="document")

    def __init__(self, documentid, countrylanguage):
        self.documentid = documentid
        self.countrylanguage = countrylanguage