from datetime import date
import logging
from sets import Set

from django.test import TestCase
from django.test import client
from django.utils import simplejson

from library.models import *
from library import utils
from library.utils import pandora

class Tests(TestCase):

    def setUp(self):
        self.logger = logging.getLogger()

    def test_release_group_no_releases(self):
        '''
        http://github.com/aroscoe/music-inbox/issues#issue/1
        tests release groups that don't have any releases
        '''
        artist = MBArtist.objects.create(name = 'Galactic', mb_id = 'http://musicbrainz.org/artist/cabbdf87-5cb2-4f3c-be65-254655c87508.html')
        self.assertEquals((None, None),
                          artist.get_release_date('http://musicbrainz.org/release-group/32195cf1-5d5c-412e-b308-1d586c08e6c4.html', logger))

        
    def test_null_release_dates(self):
        '''
        makes sure the Library._newest_ function can accept null MBAlbum.release_date's
        '''
        
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


    def test_fetch_albums(self):
        artist = MBArtist.objects.create(name='4 Non Blondes',
                                         mb_id='http://musicbrainz.org/artist/efef848b-63e4-4323-8ef7-69a48fbdd51d')
        artist.fetch_albums(logger)
        self.assertEquals(1, len(MBAlbum.objects.all()))
        album = MBAlbum.objects.get(name='Bigger, Better, Faster, More!')
        self.assertNotEquals(None, album)
        self.assertEquals('http://musicbrainz.org/release-group/0d26ee11-05f3-3a02-ba40-1414fa325554',
                          album.mb_id)
        self.assertEquals(date(1992, 10, 13), album.release_date)
        self.assertEquals(artist, album.artist)


    def test_get_release_date(self):
        artist = MBArtist.objects.create(name='4 Non Blondes',
                                         mb_id='http://musicbrainz.org/artist/efef848b-63e4-4323-8ef7-69a48fbdd51d')
        release_date, asin = artist.get_release_date('http://musicbrainz.org/release-group/0d26ee11-05f3-3a02-ba40-1414fa325554', logger)
        self.assertEquals(date(1992, 10, 13), release_date)
        
        
    def test_lookup_artist_for_new_artist(self):
        library = Library.objects.create(name='test')
        artist = library.artist_set.create(name='4 Non Blondes')
        
        lookup_artist(artist, self.logger)
        
        self.assertEquals('http://musicbrainz.org/artist/efef848b-63e4-4323-8ef7-69a48fbdd51d', artist.mb_artist_id)
        
        mb_artist = MBArtist.objects.get(name='4 Non Blondes')
        self.assertNotEquals(None, mb_artist)
        self.assertEquals('http://musicbrainz.org/artist/efef848b-63e4-4323-8ef7-69a48fbdd51d',
                          mb_artist.mb_id)
        
        self.assertEquals(1, len(MBAlbum.objects.all()))
        album = MBAlbum.objects.get(name='Bigger, Better, Faster, More!')
        self.assertNotEquals(None, album)
        self.assertEquals('http://musicbrainz.org/release-group/0d26ee11-05f3-3a02-ba40-1414fa325554',
                          album.mb_id)
        self.assertEquals(date(1992, 10, 13), album.release_date)
        self.assertEquals(mb_artist, album.artist)
        
    def test_lookup_artist_for_existing_artist(self):
        mb_artist = MBArtist.objects.create(name='4 Non Blondes',
                                            mb_id='http://musicbrainz.org/artist/efef848b-63e4-4323-8ef7-69a48fbdd51d')
        library = Library.objects.create(name='test')
        artist = library.artist_set.create(name='4 Non Blondes')

        lookup_artist(artist, self.logger)
        
        self.assertEquals(mb_artist.mb_id, artist.mb_artist_id)
        # albums should not be fetched
        self.assertEquals(0, len(MBAlbum.objects.all()))

    def test_lookup_artist_for_new_artist_fixes_name(self):
        library = Library.objects.create(name='test')
        artist = library.artist_set.create(name='4 non blondes')
        
        lookup_artist(artist, self.logger)
        
        self.assertEquals('4 Non Blondes', artist.name)

    def test_missing_albums(self):
        mb_artist = MBArtist.objects.create(mb_id='http://musicbrainz.org/artist/5e521e8c-0ab2-44c4-8fd8-14d8d3321265',
                                            name='Isis')

        celestial = MBAlbum.objects.create(mb_id='http://musicbrainz.org/release-group/e371d1e5-8737-3c79-a16e-0d4c487eedfd',
                                           artist=mb_artist,
                                           name='Celestial',
                                           release_date='2000-07-19',
                                           asin='B00008RWXM')
        
        oceanic = MBAlbum.objects.create(mb_id='http://musicbrainz.org/release-group/2426e089-b3e2-3513-b43e-f1b73fb54e60',
                                         artist=mb_artist,
                                         name='Oceanic',
                                         release_date='2002-09-17',
                                         asin='B00006IQHQ')
        panopticon = MBAlbum.objects.create(mb_id='http://musicbrainz.org/release-group/4d0ec287-514f-32bc-8939-2705f49ca44c',
                                            artist=mb_artist,
                                            name='Panopticon',
                                            release_date='2004-10-19',
                                            asin='B0002Z83KC')
        absence = MBAlbum.objects.create(mb_id='http://musicbrainz.org/release-group/bd21552f-34ac-37bf-b53f-10f7c8bd043d',
                                         artist=mb_artist,
                                         name='In the Absence of Truth',
                                         release_date='2006-01-01',
                                         asin='')
        radiant = MBAlbum.objects.create(mb_id='http://musicbrainz.org/release-group/750d7870-f7eb-3a50-8b3d-2e0e8eb4a981',
                                         artist=mb_artist,
                                         name='Wavering Radiant',
                                         release_date='2009-04-21',
                                         asin='B001SZ298M')

        library = Library.objects.create(name='test')
        artist = library.artist_set.create(name='Isis')
        album = artist.album_set.create(name='Wavering Radiant')

        lookup_artist(artist, self.logger)

        # fetch album from db again
        album = list(artist.album_set.all())[0]

        self.assertEquals(radiant.mb_id, album.mb_id)

        missing_albums = library.missing_albums()

        self.assertFalse(radiant in missing_albums)
        self.assertTrue(oceanic in missing_albums)
        self.assertTrue(absence in missing_albums)
        self.assertTrue(panopticon in missing_albums)
        self.assertTrue(celestial in missing_albums)

class HttpTests(TestCase):
    '''Client tests that make http requests and verify the right responses.''' 
    
    def setUp(self):
        self.client = client.Client()


    def test_post_form_and_rss(self):
        '''Uploads library data via the form api and verifies that the an rss
        uri is returned correctly. Then verifies that the new release is in the 
        rss feed.
        
        '''

        mb_artist = MBArtist.objects.create(mb_id='http://musicbrainz.org/artist/5e521e8c-0ab2-44c4-8fd8-14d8d3321265',
                                            name='Isis')

        celestial = MBAlbum.objects.create(mb_id='http://musicbrainz.org/release-group/e371d1e5-8737-3c79-a16e-0d4c487eedfd',
                                           artist=mb_artist,
                                           name='Celestial',
                                           release_date='2000-07-19',
                                           asin='B00008RWXM')
        
        oceanic = MBAlbum.objects.create(mb_id='http://musicbrainz.org/release-group/2426e089-b3e2-3513-b43e-f1b73fb54e60',
                                         artist=mb_artist,
                                         name='Oceanic',
                                         release_date='2002-09-17',
                                         asin='B00006IQHQ')

        response = self.client.post('/api/library/form/', {'name': 'test_lib',
                                                           'Isis': 'Celestial' })
        self.assertEquals('application/json; charset=utf-8', 
                          response['Content-Type'])
        json = simplejson.loads(response.content, 'utf-8')
        self.assertTrue('rssUri' in json)
        self.assertEquals('http://example.com/library/feeds/newalbums/5013407824245992320/', 
                          json['rssUri'])
        
        response = self.client.get('/library/feeds/newalbums/5013407824245992320/')
        # should contain 'Oceanic' release
        self.assertTrue('Oceanic' in response.content)

    def test_get_non_existant_rss_feed_not_found(self):
        '''Asserts that a GET request on a non existant rss feed returns 404
        error code.

        '''
        response = self.client.get('/library/feeds/newalbums/5013407824245992320/')
        self.assertEquals(404, response.status_code)


class PandoraTests(TestCase):
    '''Test for the pandora module.'''
    
    # TODO: create more Pandora tests
    
    def setUp(self):
        pass
    
    def test_fetch_artists_fetches_everything(self):
        artists = pandora.fetch_artists('john')
        expected_artists = Set(["Radiohead", "Joshua Radin", "The National", "Yaz", "Prince", "Travis", "Vega4", "Supermen Lovers", "Massive Attack", "Alex Lloyd", "Downtown Singapore", "Kate Nash", "Porcupine Tree", "The Dandy Warhols", "Stars", "Math And Physics Club", "Jem", "The Shins", "Supreme Beings Of Leisure", "Information Society", "Moloko", "Alex Parks", "Frou Frou", "Ray LaMontagne", "Bitter:Sweet", "Duran Duran", "New Order", "Sixth Finger", "John Legend", "Kylie Minogue", "Pernice Brothers", "Andrew Bird", "The Jacksons", "Frou Frou", "Cake", "Jack Penate", "Telepopmusik", "Pelle Carlberg", "Moloko", "Emiliana Torrini", "Arctic Monkeys", "Goldenboy", "The Rosewood Thieves", "Delerium", "Letters To Cleo", "Jessica Simpson", "The Perishers", "Interpol", "Aqualung", "Edel & Weiss", "DNA", "The 1900s", "Tiga", "Robbie Rivera", "The Apples In Stereo", "Train"])
        self.assertTrue(expected_artists.issubset(artists))
    
