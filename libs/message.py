from django.http import HttpResponse
from django.utils import simplejson

class Message:
    """
    Generic message class that will output to JSON
    
    Status Codes
    0: error
    1: complete
    2: partial
    
    """
    def __init__(self, data, status=1):
        self.data = {'status': status, 'data': data}
    
    def __getitem__(self, key):
        return self.data[key]
    
    def __setitem__(self, key, item):
        self.data[key] = item
    
    def get_data(self):
        return self.data

class JSONMessage(Message):
    """
    JSON message
    """
    def get_response(self):
        return HttpResponse(simplejson.dumps(self.data), mimetype='application/json')
