from DB.base import Base
from sqlalchemy import Column, String, Boolean, Integer, Sequence, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy import ForeignKeyConstraint

class Introduction(Base):
    __tablename__ = 'introduction'

    # emits CREATE SEQUENCE + INTEGER
    introductionid = Column(Integer, Sequence('introduction_id_seq'), primary_key=True)
    text = Column(String)
    item_name = Column(String)


    def __init__(self, text, item_name):
        self.text = text
        self.item_name = item_name