from base import Base
from sqlalchemy import Column, String, Integer, Sequence, ForeignKey
from sqlalchemy.orm import relationship, backref

class ScaleItem(Base):
    __tablename__ = 'scaleitem'

    # emits CREATE SEQUENCE + INTEGER
    scaleitemid = Column(Integer, Sequence('scale_item_id_seq'), primary_key=True)
    scaleid = Column(Integer, ForeignKey('scale.scaleid'))
    scaleitem = Column(String)
    scale = relationship("Scale", backref=backref("scaleitem", uselist=False))


    def __init__(self, scaleid, scaleitem):
        self.scaleid = scaleid
        self.scaleitem = scaleitem