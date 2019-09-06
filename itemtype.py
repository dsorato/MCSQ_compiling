from base import Base

class ItemType(Base):
    __tablename__ = 'itemtype'

    # emits CREATE SEQUENCE + INTEGER
    itemtypeid = Column(Integer, Sequence('type_id_seq'), primary_key=True)
    itemtype = Column(String)
    itemtypeisresponse = Column(Boolean)

    def __init__(self, itemtype, itemtypeisresponse):
        self.itemtype = itemtype
        self.itemtypeisresponse = itemtypeisresponse
