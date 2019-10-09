from base import Base
from sqlalchemy import Column, String, Integer, Sequence, ForeignKey

class TextItem(Base):
    __tablename__ = 'textitem'

    # emits CREATE SEQUENCE + INTEGER
    textitemid = Column(Integer, Sequence('text_item_id_seq'), primary_key=True)
    text = Column(String)


    def __init__(self, text):
        self.text = text