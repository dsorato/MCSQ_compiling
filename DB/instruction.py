from DB.base import Base
from sqlalchemy import Column, String, Boolean, Integer, Sequence, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy import ForeignKeyConstraint

class Instruction(Base):
    __tablename__ = 'instruction'

    # emits CREATE SEQUENCE + INTEGER
    instructionid = Column(Integer, Sequence('instruction_id_seq'), primary_key=True)
    text = Column(String)
   

    def __init__(self, text):
        self.text = text
