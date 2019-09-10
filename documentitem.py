from base import Base
from sqlalchemy import Column, String, Boolean, Integer, Sequence, ForeignKey
from sqlalchemy.orm import relationship, backref


class DocumentItem(Base):
    __tablename__ = 'documentitem'

    # emits CREATE SEQUENCE + INTEGER
    documentitemid = Column(Integer, Sequence('document_item_id_seq'), primary_key=True)
    documentid = Column(String, ForeignKey('document.documentid'))
    itemtypeid = Column(Integer, ForeignKey('itemtype.itemtypeid'))
    text = Column(String)
    morethanonetranslation = Column(Boolean)
    translation2 = Column(String)
    translation3 = Column(String)
    translationadjudication = Column(String)
    translationverification = Column(String)
    translationdescription = Column(String)
    translationupdated = Column(Boolean)
    document = relationship("Document", backref=backref("documentitem", uselist=False))
    itemtype = relationship("ItemType", backref="documentitem")

    def __init__(self, documentid, itemtypeid, text, morethanonetranslation, translation2, translation3, translationadjudication, 
        translationverification, translationdescription, translationupdated):
        self.documentid = documentid
        self.itemtypeid = itemtypeid
        self.text = text
        self.morethanonetranslation = morethanonetranslation
        self.translation2 = translation2
        self.translation3 = translation3
        self.translationadjudication = translationadjudication
        self.translationverification = translationverification
        self.translationdescription = translationdescription
        self.translationupdated = translationupdated
        
