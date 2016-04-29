'''
Created on Apr 26, 2016

@author: deaconpham
'''
import json
from sqlalchemy import create_engine, exc, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import sessionmaker

DB_CONN = "postgresql://myprojectuser:Admin123@localhost/myproject"

Base = declarative_base()
    
class PixelEvent(Base):
    __tablename__ = 'pixel_event'
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer)
    customer_id = Column(Integer)
    doc = Column(JSONB)
        
# create pixel tracking tables if not already there
def initializeTables():
                
    # connect to engine
    engine = create_engine(DB_CONN)

    # create tables
    Base.metadata.create_all(engine)
    
    
