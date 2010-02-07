from django.test import TestCase

class Tests(TestCase):
    def test_views_missing(self):

        from library.views import *
        from django.http import Http404
        try:
            missing(None, 1).status_code
            raise Exception('should have thrown Http404')
        except Http404:
            print 'expected result'
        
        from library.models import *
        Library.objects.create(pk=1, name='foo')
    
        self.failUnlessEqual('{"processing": 2}', missing(None, 1).content)

                               
