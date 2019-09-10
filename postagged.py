from base import Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship, backref

class PoSTaggedText(Base):
    __tablename__ = 'postaggedtext'

    documentitemid = Column(String, ForeignKey('documentitem.documentitemid'))
    postag = Column(String)
    documentitem = relationship("DocumentItem", backref=backref("postaggedtext", uselist=False))

    def __init__(self, documentitemid, postag):
        self.documentitemid = documentitemid
        self.postag = postag
