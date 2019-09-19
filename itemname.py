from base import Base
from sqlalchemy import Column, String, Integer, Sequence

class ItemName(Base):
    __tablename__ = 'itemname'

    itemnameid = Column(Integer, Sequence('item_name_id_seq'), primary_key=True)
    itemname = Column(String)


    def __init__(self, itemname):
        self.itemname = itemname
