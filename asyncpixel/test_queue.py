'''
Created on Apr 26, 2016

@author: deaconpham
'''
import time
import pytest
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import Session, sessionmaker, Query
from .orm import initializeTables, PixelEvent
from _pytest.python import fixture

from pixtrack.queue import QueueManager, PixelEventLogger
from pixtrack.orm import PixelEvent, DB_CONN


@pytest.fixture(scope="session")
def engine():
    """ override DB_CONN to different connection string if want to use a test db instance
    current set to: postgresql://myprojectuser:Admin123@localhost/myproject"
    """
    engine = create_engine(DB_CONN)
    return engine

def _clean_tables(engine):
#     conn = engine.connect()
#     pixel_event = PixelEvent()
#     result = conn.execute(pixel_event.delete())
    Session = sessionmaker(engine)
    session = Session()
    rowcount = session.query(PixelEvent).delete()
    session.commit()
    print("result row count = " + str(rowcount))

def test_singleton():
    queue_mgr1 = QueueManager()
    queue_mgr2 = QueueManager()
    queue_mgr3 = QueueManager()
    assert queue_mgr1 == queue_mgr2 == queue_mgr3
    
def test_save_pixelevent(engine):
    # delete any rows in db with accountId and customerId is 1000001
    Session = sessionmaker(engine)
    session = Session()
    session.query(PixelEvent).filter(and_(PixelEvent.account_id==1000001, PixelEvent.customer_id==1000001)).delete()
    session.commit()
    
    queue_mgr = QueueManager()
    msg = '{"stringone": ["test_save_message"], "accountId": ["1000001"], "customerId": ["1000001"], "stringtwo": ["test_save_message"]}'    
    queue_mgr.queue.put(msg)
    time.sleep(1) # give time for queue mgr logger thread to pick up queue item
    queue_mgr.kill_loggers = True
    
    query = session.query(PixelEvent).filter(and_(PixelEvent.account_id==1000001, PixelEvent.customer_id==1000001))
    pixelevent = query[0]
    assert isinstance(pixelevent, PixelEvent)
    assert query.count() == 1
    
    session.delete(pixelevent)
    session.commit()
    
    
    
# def test_not_json_message():
#     queue_mgr = QueueManager()
#     msg = [0]
#     queue_mgr.queue.put(msg)
#     
#     pixlogger = PixelEventLogger(queue_mgr)
        
        
        
        