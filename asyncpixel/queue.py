'''
Created on Apr 26, 2016

@author: deaconpham
'''
import logging
from queue import Queue
import threading
import json
import time
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import Session, sessionmaker
from pixtrack import orm
from pixtrack.orm import PixelEvent, DB_CONN


# manages the queue & workers
class QueueManager:
    
    kill_loggers = False
    
    # singleton pattern to ensure only 1 instance of manager
    __instance = None
    def __new__(cls):
        if QueueManager.__instance is None:
            QueueManager.__instance = object.__new__(cls)
        return QueueManager.__instance
    
    def __init__(self):
        # initialize queue and workers
        self.queue = Queue()
        self.event_logger = PixelEventLogger(self);
        logger = logging.getLogger(__name__)
        logger.info("QueueManager initialized")

        self.thread1 = threading.Thread(target=self.event_logger.begin)
        self.thread1.daemon = True
        self.thread1.start()
        
        logger.info("1 PixelEventLogger started")
             
    # TODO: need to decide where to put initializeTables function             
    def initializeTables(self):
        orm.initializeTables()
            

    
class PixelEventLogger:

    def __init__(self, queue_mgr):
        self.queue_mgr = queue_mgr
        logger = logging.getLogger(__name__)
        logger.info("Starting PixelEventLogger instance and thread.")
        
    def begin(self):
        logger = logging.getLogger(__name__)
        # get item from queue and persist. TODO: need to catch exception from .get_nowait()
        while self.queue_mgr.kill_loggers is False:   
            # item should be a json in string form
            item = self.queue_mgr.queue.get()
            if item is None or not isinstance(item, str):
                logger.debug("PixelEventLogger.begin: about to sleep for 1 second")
                time.sleep(1);                          
            self._persist(item)
            
        
    def _persist(self, json_str):
        logger = logging.getLogger(__name__)
        if json_str is None:
            return
        
        engine = create_engine(DB_CONN)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        json_obj = json.loads(json_str)
        
        # dummy id's if none provided. TODO FIX AFTER PROTOTYPE
        # getting an element from json object returns a 'list', not a single element
        acct_id = json_obj['accountId']
        if acct_id is None or not self.represents_int(acct_id[0]):
            logger.debug("PixelEventLogger._persist: account Id provided was invalid. Seeting to default value 0")
            account_id = 0
        else:
            account_id = acct_id[0]
        cust_id = json_obj['customerId']
        if cust_id is None or not self.represents_int(cust_id[0]):
            logger.debug("PixelEventLogger._persist: customer Id provided was invalid. Seeting to default value 0")            
            customer_id = 0
        else:
            customer_id = cust_id[0]
    
        logger.debug("PixelEventLogger._persist: Saving pixel event..." + json_str)
        pixevent = PixelEvent(account_id=account_id, customer_id=customer_id, doc=json_obj)
        
        session.add(pixevent)  
        session.commit()
        
        # TODO: add db related exception handling
    
    # helper function
    def represents_int(self, s):        
        try: 
            int(s)
            return True
        except ValueError:
            return False   

    
    # ALTERNATE WAY TO CREATE SINGLETON
#     class __QueueManager:
#         def __init__(self):
#             self.val = None
#         def __str__(self):
#             return 'self' + self.val
#     instance = None
#     def __new__(cls):
#         if not QueueManager.instance:
#             QueueManager.instance = QueueManager.__QueueManager()
#         return