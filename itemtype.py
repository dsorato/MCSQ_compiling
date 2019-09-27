from base import Base
from sqlalchemy import Column, String, Boolean, Integer, Sequence, ForeignKey

class ItemType(Base):
    __tablename__ = 'itemtype'

    # emits CREATE SEQUENCE + INTEGER
    itemtypeid = Column(Integer, Sequence('type_id_seq'), primary_key=True)
    itemtype = Column(String)
    itemtypeisresponse = Column(Boolean)
    itemtypehasscale = Column(Boolean)
    scaletype = Column(String)

    def __init__(self, itemtype, itemtypeisresponse, itemtypehasscale, scaletype):
        self.itemtype = itemtype
        self.itemtypeisresponse = itemtypeisresponse
        self.itemtypehasscale = itemtypehasscale
        self.scaletype = scaletype
