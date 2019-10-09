from base import Base
from sqlalchemy import Column, String, Boolean, Integer, Sequence, ForeignKey
from sqlalchemy.orm import relationship, backref


class TextItemDraft(Base):
    __tablename__ = 'textitemdraft'

    # emits CREATE SEQUENCE + INTEGER
    textitemdratfid = Column(Integer, Sequence('text_item_draft_id_seq'), primary_key=True)
    textitemid = Column(Integer, ForeignKey('textitem.textitemid'))
    translation2 = Column(String)
    translation3 = Column(String)
    translationverification = Column(String)
    textitem = relationship("TextItem", backref=backref("textitemdraft", uselist=False))

    def __init__(self, textitemid, translation2, translation3, translationverification):
        self.textitemid = textitemid
        self.translation2 = translation2
        self.translation3 = translation3
        self.translationverification = translationverification
        
