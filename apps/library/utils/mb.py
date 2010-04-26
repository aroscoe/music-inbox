import logging
import time
from datetime import date

from django.conf import settings
import musicbrainz2.webservice as ws
import musicbrainz2.model as m

from library.models import *

logging.basicConfig()
logger = logging.getLogger("album_diff")

def album_diff(library):
    logger.setLevel(settings.LOG_LEVEL)
    logger.debug("processing " + library.name + " ...")
    
    for artist in library.artist_set.order_by("-play_count"):
        lookup_artist(artist)

def lookup_artist(artist):
    logger.debug(artist.name + " ...")
    name_filter = ws.ArtistFilter(name=artist.name, limit=5)
    q = ws.Query()
    # query 1 get list of matching artists from mb
    # could do lookup in db first
    artist_results = call_mb_ws(q.getArtists, name_filter)
    time.sleep(settings.SLEEP_TIME)
    if artist_results:
        mb_artist_id = artist_results[0].artist.id
        artist.mb_artist_id = mb_artist_id
        artist.save()
        
        # query for each single album that the user has
        for release_group in artist.album_set.all():
            get_release_group_id(release_group, mb_artist_id)
            
        mb_artist_entry, created_artist = MBArtist.objects.get_or_create(mb_id=mb_artist_id)
        if created_artist:
            mb_artist_entry.name = artist.name
            mb_artist_entry.save()
            
            mb_artist_entry.fetch_albums()
                
def get_release_group_id(album, mb_artist_id):
    releases = get_releases(album.name, mb_artist_id)
    time.sleep(settings.SLEEP_TIME)
    if releases:
            includes = ws.ReleaseIncludes(releaseGroup=True)
            q = ws.Query()
            id = call_mb_ws(q.getReleaseById, releases[0].release.id, includes).releaseGroup.id
            time.sleep(settings.SLEEP_TIME)
            album.mb_id = id;
            album.save()
            return id
    return None

def get_releases(name, mb_artist_id):
    release_filter = ws.ReleaseFilter(
                            title=name,
                            artistId=mb_artist_id,
                            releaseTypes=(m.Release.TYPE_OFFICIAL,
                                    m.Release.TYPE_ALBUM))
    q = ws.Query()
    return call_mb_ws(q.getReleases, release_filter)

def call_mb_ws(function, *args):
    i = 1
    while True:
        try:
            return function(*args)
        except ws.WebServiceError, e:
            if '503' in message:
                logger.debug('function ' + function.func_name + ' failed with 503, sleeping ' + str(settings.SLEEP_TIME * i) + ' seconds')
                time.sleep(settings.SLEEP_TIME * i)
                i *= 2
            else:
                raise e
 
