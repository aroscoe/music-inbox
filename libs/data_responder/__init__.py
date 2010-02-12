from django.utils import simplejson
from django.http import HttpResponse

class JSONDataResponder(object):
    """
    Generic JSON Responder
    
    This is built from SerializeResponder but accepts any dictionary.
    """
    format = 'json'
    mimetype = 'application/json'
    PROCESSING_CODES = [0,1,2]
    
    def __init__(self, data_dict=None, processing=1):
        """
        data_dict:
            Dictionary used to populate the data you want returned in the JSON response.
        processing:
            Processing code, used to determine what state the information you are getting back is in.
            0: Error has occured
            1: Processing complete
            2: Information is currently processing.
        """
        self.data_dict = {
            'processing': '',
            'data': {}
        }
        if data_dict: self.add_data(data_dict)
        
        self._set_processing(processing)
    
    def add_data(self, data_dict):
        self.data_dict['data'].update(data_dict)
    
    def _get_response(self):
        response = HttpResponse(mimetype=self.mimetype)
        simplejson.dump(self.data_dict, response)
        return response
    
    response = property(_get_response)
    
    def _get_processing(self):
        return self.data_dict['processing']
    
    def _set_processing(self, value):
        if not value in self.PROCESSING_CODES: raise ValueError("Processing value not valid.")
        self.data_dict['processing'] = value
    
    processing = property(_get_processing, _set_processing)
