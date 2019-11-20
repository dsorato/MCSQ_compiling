from base import Base
from sqlalchemy import Column, String, Boolean, Integer, Sequence, ForeignKey
from sqlalchemy.orm import relationship, backref

class Error_message(Base):
    __tablename__ = 'error_message'

	# emits CREATE SEQUENCE + INTEGER
    errorid = Column(Integer, Sequence('error_message_id_seq'), primary_key=True)
    surveyid = Column(String, ForeignKey('survey.surveyid'))
    error_label = Column(String)
    message = Column(String)

    survey = relationship("Survey", backref=backref("error_message", uselist=False))

    def __init__(self, surveyid, error_label, message):
        self.surveyid = surveyid
        self.error_label = error_label
        self.message = message