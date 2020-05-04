from DB.base import Base
from sqlalchemy import Column, String, Boolean, Integer, Sequence, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy import ForeignKeyConstraint

class Instruction(Base):
    __tablename__ = 'instruction'

    # emits CREATE SEQUENCE + INTEGER
    instructionid = Column(Integer, Sequence('instruction_id_seq'), primary_key=True)
    survey_itemid = ForeignKeyConstraint(['survey_itemid', 'survey_unique_itemid'], ['survey_item.survey_itemid', 'survey_item.survey_unique_itemid'])
    final_text = Column(String)
    translation_1 = Column(String)
    translation_2 = Column(String)
    review = Column(String)
    adjudication = Column(String)
    item_name = Column(String)
    item_type = Column(String)


    # survey_item = relationship("Survey_item", backref=backref("instruction", uselist=False))

    def __init__(self, survey_itemid, final_text, translation_1, translation_2, review, adjudication, item_name, item_type):
        self.survey_itemid = survey_itemid
        self.final_text = final_text
        self.translation_1 = translation_1
        self.translation_2 = translation_2
        self.review = review
        self.adjudication = adjudication
        self.item_name = item_name
        self.item_type = item_type