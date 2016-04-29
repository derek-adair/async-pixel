'''
Created on Apr 23, 2016

@author: deaconpham
'''
import logging
from abc import ABCMeta
from aiohttp import web
from aiohttp.web_reqrep import Request
from urllib import parse 
import json 
from pixtrack.queue import QueueManager


# Deffered TO-DO Task List
# - sufficient test casdesss
# - add exceptions 
# -  



# abstract class that processes a aiohttp request/response pair
class AbstractProcessor(metaclass=ABCMeta):
    
    def preProcess(self, request, response, *args, **kwargs):
        pass
    
    def postProcess(self, request, response, *args, **kwargs):
        pass
    
    def process(self, request, response, *args, **kwargs):
        pass
    
class VisitorProcessor(AbstractProcessor):
    
    def process(self, request, response, *args, **kwargs):
        response.text = response.text + "\n  Hi! I'm inside object of class VisitorProcessor"
        pass


class TrackingEventProcessor(AbstractProcessor):
    
    def process(self, request, response, *args, **kwargs):
        logger = logging.getLogger(__name__)
        
        # parse query parameters
        qs = request.query_string
        parsed_qs = parse.parse_qs(qs)       
        pixelevent_json = json.dumps(parsed_qs)   
        
        queue_mgr = None
        #queuemgr = QueueManager()
        if kwargs is not None:
            queue_mgr = kwargs['queue_mgr']
        else:
            # need to throw an error here
            logger.debug("TrackingEvent")
            pass
        
        queue_mgr.queue.put(pixelevent_json)
                
        # TODO: need to remove these messages and just return pixel        
        response.text = response.text + "\n  Hi! I'm inside object of class TrackingEventProcessor"
        response.text = response.text + "\n     and query string is ... " + qs
        response.text = response.text + "\n     and the request query string in json is ..." + pixelevent_json
        

class ProcessorChain():
    
    def __init__(self, chain=None):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
        # if no chain passed in, initiate default chain        
        self._chain = chain
        if self._chain == None:
            self._chain = [VisitorProcessor(), TrackingEventProcessor()]

        
    def executeChain(self, request, response, *args, **kwargs):
        
        for processor in self._chain:
            processor.process(request, response, *args, **kwargs)
            
            
            
            
            