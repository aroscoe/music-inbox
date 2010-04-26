from django.test import TestCase

class Tests(TestCase):
    def test_views_missing(self):
        print 'running'
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
        from musicbrainz2.webservice import *
        artist = MBArtist.objects.create(name = 'Galactic', mb_id = 'http://musicbrainz.org/artist/cabbdf87-5cb2-4f3c-be65-254655c87508.html')
        self.assertRaises(ResourceNotFoundError, 
                          artist.get_release_date, 
                          'http://musicbrainz.org/release-group/32195cf1-5d5c-412e-b308-1d586c08e6c4.html')
        
        
    def test_null_release_dates(self):
        '''
        makes sure the Library._newest_ function can accept null MBAlbum.release_date's
        '''
        from library.models import *
        from datetime import datetime
        import sys
        
        artist = MBArtist.objects.create(name = 'foo', mb_id = 'http://bar.baz')
        # null release dates
        album1 = MBAlbum.objects.create(name = 'bar', mb_id = 'http://bar.com/album1', artist = artist)
        album2 = MBAlbum.objects.create(name = 'bar', mb_id = 'http://bar.com/album2', artist = artist)
        
        # non-null release date
        album3 = MBAlbum.objects.create(name = 'bar', mb_id = 'http://bar.com/album3', artist = artist, release_date = datetime.now())
        
        library = Library.objects.create(pk = 1, name = 'foo')

        self.assertEquals(-sys.maxint, library._newest_(album1, album2))
        self.assertEquals(sys.maxint, library._newest_(album1, album3))
        self.assertEquals(-sys.maxint, library._newest_(album3, album2))
