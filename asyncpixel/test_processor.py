'''
Created on Apr 24, 2016

@author: deaconpham
'''
import pytest
from unittest.mock import MagicMock, patch
from aiohttp.web import Request, Response

from pixtrack.processor import TrackingEventProcessor, QueueManager


class TestProcessTrackingEvent:
    
    @patch('aiohttp.web.Response')
    @patch('aiohttp.web.Request')
    def test_req_query_str(self, mock_request, mock_response):
        processor = TrackingEventProcessor()   
        queue_mgr = QueueManager()

        mock_request.configure_mock(query_string="accountId=1&customerID=1&stringone=1&stringtwo=2")
        
        # remove this text value after refactor ProcessorTrackingEvent class
        textValue = "Hi! I'm from the responseMock object!"        
        mock_response.configure_mock(text=textValue) 
                                
        processor.process(mock_request, mock_response, queue_mgr=queue_mgr)    
    
        assert textValue in mock_response.text

        # get item from queue and assert

    def test_queue_msg(self):
        pass


