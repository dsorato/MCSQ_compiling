from base import Base

class Module(Base):
    __tablename__ = 'module'

    # emits CREATE SEQUENCE + INTEGER
    moduleid = Column(Integer, Sequence('module_id_seq'), primary_key=True)
    modulename = Column(String)

    def __init__(self, modulename):
        self.modulename = modulename
