from base import Base
from sqlalchemy import Column, String, Boolean, Integer, Sequence, ForeignKey
from sqlalchemy.orm import relationship, backref


class DocumentItem(Base):
    __tablename__ = 'documentitem'

    # emits CREATE SEQUENCE + INTEGER
    documentitemid = Column(Integer, Sequence('document_item_id_seq'), primary_key=True)
    documentid = Column(String, ForeignKey('document.documentid'))
    texttitemid = Column(Integer, ForeignKey('textitem.textitemid'))
    itemtypeid = Column(Integer, ForeignKey('itemtype.itemtypeid'))
    itemnameid = Column(Integer, ForeignKey('itemname.itemnameid'))
    translationupdated = Column(Boolean)
    mode = Column(String)
    translationdescription = Column(String)
    
    
    document = relationship("Document", backref=backref("documentitem", uselist=False))
    textitem = relationship("TextItem", backref="documentitem")
    itemtype = relationship("ItemType", backref="documentitem")
    itemname = relationship("ItemName", backref="documentitem")


    def __init__(self, documentid, texttitemid, itemtypeid, itemnameid, translationupdated, mode, translationdescription):
        self.documentid = documentid
        self.texttitemid = texttitemid
        self.itemtypeid = itemtypeid
        self.itemnameid = itemnameid
        self.translationupdated = translationupdated
        self.mode = mode
        self.translationdescription = translationdescription

        
        
