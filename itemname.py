from base import Base
from sqlalchemy import Column, String, Boolean, Integer, Sequence, ForeignKey

class ItemType(Base):
    __tablename__ = 'itemtypename'

    documentitemid = Column(Integer, ForeignKey('documentitem.documentitemid'))
    itemname = Column(String)
    documentitem = relationship("DocumentItem", backref="itemtypename")


    def __init__(self, documentitemid, itemname):
        self.documentitemid = documentitemid
        self.itemname = itemname
