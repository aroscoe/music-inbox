from django.test import TestCase

class Tests(TestCase):
    def test_views_missing(self):
        from api.views import *
        from django.http import Http404
        try:
            missing(None, 1).status_code
            raise Exception('should have thrown Http404')
        except Http404:
            print 'expected result'
        
        from library.models import *
        Library.objects.create(pk=1, name='foo')
        
        self.assertEqual('{"processing": 2, "data": {}}', missing(None, 1).content)

    def test_release_group_no_releases(self):
        '''
        http://github.com/aroscoe/music-inbox/issues#issue/1
        tests release groups that don't have any releases
        '''
        from library.models import *
        artist = MBArtist.objects.create(name = 'Galactic', mb_id = 'http://musicbrainz.org/artist/cabbdf87-5cb2-4f3c-be65-254655c87508.html')
        date, asin = artist.get_release_date('http://musicbrainz.org/release-group/32195cf1-5d5c-412e-b308-1d586c08e6c4.html')
        self.assertEqual(None, date)
        self.assertEqual(None, asin)
