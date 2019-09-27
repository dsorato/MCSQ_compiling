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
    translationdescription = Column(String)
    translationupdated = Column(Boolean)
    mode = Column(String)
    itemnameid = Column(Integer, ForeignKey('itemname.itemnameid'))
    document = relationship("Document", backref=backref("documentitem", uselist=False))
    itemtype = relationship("ItemType", backref="documentitem")
    itemname = relationship("ItemName", backref="documentitem")

    def __init__(self, documentid, itemtypeid, text, translationdescription, translationupdated, mode, itemnameid):
        self.documentid = documentid
        self.itemtypeid = itemtypeid
        self.text = text
        self.translationdescription = translationdescription
        self.translationupdated = translationupdated
        self.itemnameid = itemnameid
        
