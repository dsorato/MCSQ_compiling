from DB.base import Base
from sqlalchemy import Column, String, Boolean, Integer, Sequence, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy import ForeignKeyConstraint

class Introduction(Base):
    __tablename__ = 'introduction'

    # emits CREATE SEQUENCE + INTEGER
    introductionid = Column(Integer, Sequence('introduction_id_seq'), primary_key=True)
    survey_unique_itemid = Column(Integer, nullable=False)
    survey_itemid = Column(String, nullable=False)
    ForeignKeyConstraint(['survey_itemid', 'survey_unique_itemid'], ['survey_item.survey_itemid', 'survey_item.survey_unique_itemid'])
    final_text = Column(String)
    translation_1 = Column(String)
    translation_2 = Column(String)
    review = Column(String)
    adjudication = Column(String)
    item_name = Column(String)
    item_type = Column(String)

    # survey_item = relationship("Survey_item", backref=backref("introduction", uselist=False))

    def __init__(self, survey_unique_itemid, survey_itemid, final_text, translation_1, translation_2, review, adjudication, item_name, item_type):
        self.survey_unique_itemid = survey_unique_itemid
        self.survey_itemid = survey_itemid
        self.final_text = final_text
        self.translation_1 = translation_1
        self.translation_2 = translation_2
        self.review = review
        self.adjudication = adjudication
        self.item_name = item_name
        self.item_type = item_type