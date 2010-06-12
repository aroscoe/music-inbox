from django.test import TestCase
from django.core.urlresolvers import reverse

class APILibraryTestCase(TestCase):
    def setUp(self):
        pass
    
    def test_library_api(self):
        response = self.client.get(reverse('api_library', args=[1234]))
        self.assertContains(response, 'Not Found', status_code=404)
        
    def test_missing_library_api(self):
        response = self.client.get(reverse('api_library_missing', args=[1234]))
        self.assertContains(response, 'Not Found', status_code=404)
