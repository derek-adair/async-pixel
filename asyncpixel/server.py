'''
Created on Apr 22, 2016

@author: deaconpham
'''
import logging
from aiohttp import web
from pixtrack.processor import QueueManager
from . import processor


# TODO: refactor logging config to use file
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='log/my_web_app.log',
                    filemode='w')
fh = logging.handlers.RotatingFileHandler("log/my_web_app.log")
logger = logging.getLogger(__name__)
logger.addHandler(fh);

# Gunicorn starts call 'server.my_web_app'
# aiohttp request handler, serving as entry point to our tracking api
async def all_handler(request):
    
    logger = logging.getLogger(__name__)
    logger.debug("Handling request ")        
            
    # instantiate response obj
    response = web.Response(text="")    
    
    # instantiate processor chain
    chain = processor.ProcessorChain()
    
    queue_mgr = QueueManager()
    
    # execute processors one by one
    chain.executeChain(request, response, queue_mgr=queue_mgr)
    
    response.text = response.text + "\n..end of all_handler"    
    
    logger.debug("...finish handling request. Returning response now.")
    return response
    

my_web_app = web.Application()
my_web_app.router.add_route('GET', '/', all_handler)
#my_web_app.router.add_route('*', '/path', all_handler)

logger.info("InPrima Pixel Tracking Server Started")