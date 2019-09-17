from base import Base
from sqlalchemy import Column, String, Integer, Sequence, ForeignKey
from sqlalchemy.orm import relationship, backref

class ItemName(Base):
    __tablename__ = 'itemname'

    documentitemid = Column(Integer, ForeignKey('documentitem.documentitemid'), primary_key=True)
    itemname = Column(String)
    documentitem = relationship("DocumentItem", backref="itemname")


    def __init__(self, documentitemid, itemname):
        self.documentitemid = documentitemid
        self.itemname = itemname
