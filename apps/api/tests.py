from django.test import TestCase
from django.core.urlresolvers import reverse

class APILibraryTestCase(TestCase):
    fixtures = ['test_library.json']
    
    def test_library_api_not_found(self):
        response = self.client.get(reverse('api_library', args=[1234]))
        self.assertContains(response, 'Not Found', status_code=404)
    
    def test_library_api_result(self):
        response = self.client.get(reverse('api_library', args=[5013407824245992320]))
        self.assertTrue('Jane Doe' in response.content)
        self.assertEquals(response.status_code, 200)
        
    def test_missing_library_api_not_found(self):
        response = self.client.get(reverse('api_library_missing', args=[1234]))
        self.assertContains(response, 'Not Found', status_code=404)
    
    def test_missing_library_api_result(self):
        response = self.client.get(reverse('api_library_missing', args=[5013407824245992320]))
        self.assertTrue('No Heroes' in response.content)
        self.assertEquals(response.status_code, 200)