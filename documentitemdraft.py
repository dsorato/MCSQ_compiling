from base import Base
from sqlalchemy import Column, String, Boolean, Integer, Sequence, ForeignKey
from sqlalchemy.orm import relationship, backref


class DocumentItemDraft(Base):
    __tablename__ = 'documentitemdraft'

    # emits CREATE SEQUENCE + INTEGER
    documentitemdratfid = Column(Integer, Sequence('document_item_draft_id_seq'), primary_key=True)
    documentitemid = Column(String, ForeignKey('documentitem.documentitemid'))
    translation2 = Column(String)
    translation3 = Column(String)
    translationadjudication = Column(String)
    translationverification = Column(String)
    documentitem = relationship("DocumentItem", backref=backref("documentitemdraft", uselist=False))

    def __init__(self, documentitemid, translation2, translation3, translationadjudication, 
        translationverification):
        self.documentitemid = documentitemid
        self.translation2 = translation2
        self.translation3 = translation3
        self.translationadjudication = translationadjudication
        self.translationverification = translationverification
        
