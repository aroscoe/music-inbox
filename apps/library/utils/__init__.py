from django.conf import settings
from django.contrib.sites.models import Site

from library import models
import tea

def decrypt_id(id, exception_to_raise):
    try:
        if not isinstance(id, long):
            id = long(id)
        return tea.decrypt(id, settings.KEY)
    except ValueError:
        raise exception_to_raise
 
def encrypt_id(id):
    return tea.encrypt(id, settings.KEY)

def rss_url(library_id):
    '''Returns the full rss url for a library_id'''
    return 'http://%s/library/feeds/newalbums/%s/' % \
        (Site.objects.get_current().domain, encrypt_id(library_id))

def scan_all_artists():
    '''Iterates through all Artist objects and checks whether their mb_id
    points to a valid MBArtist.
    
    '''
    artists = models.Artist.objects.all()
    for artist in artists:
        if artist.mb_artist_id:
            print artist
            models.MBArtist.object.get(mb_id=artist.mb_artist_id)

def scan_all_albums():
    '''Iterates over all Album objects and checks whether their mb_id
    points to a valid MBAlbum.

    '''
    albums = models.Album.objects.all()
    for album in albums:
        if album.mb_id:
            print album
            models.MBAlbum.object.get(mb_id=album.mb_id)
