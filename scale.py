from base import Base
from sqlalchemy import Column, String, Integer, Sequence, ForeignKey

class Scale(Base):
    __tablename__ = 'scale'

    # emits CREATE SEQUENCE + INTEGER
    scaleid = Column(Integer, Sequence('scale_id_seq'), primary_key=True)
    languagecountry = Column(String)


    def __init__(self, languagecountry):
        self.languagecountry = languagecountry