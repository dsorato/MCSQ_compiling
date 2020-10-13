"""
MCSQ Module table
Author: Danielly Sorato 
Author contact: danielly.sorato@gmail.com
"""

from DB.base import Base
from sqlalchemy import Column, String, Boolean, Integer, Sequence, ForeignKey

class Module(Base):
    __tablename__ = 'module'

    # emits CREATE SEQUENCE + INTEGER
    moduleid = Column(Integer, Sequence('module_id_seq'), primary_key=True)
    module_name = Column(String, nullable=False)

    def __init__(self, module_name):
        self.module_name = module_name

       
