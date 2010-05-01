import logging
import time
from datetime import date

from django.conf import settings
import musicbrainz2.webservice as ws
import musicbrainz2.model as m

from library.models import *

logging.basicConfig()
logger = logging.getLogger("album_diff")

def album_diff(library, logger):
    logger.debug("processing " + library.name + " ...")
    
    for artist in library.artist_set.order_by("-play_count"):
        lookup_artist(artist, logger)

def get_local_mb_artist(artist_name):
    '''Returns local MBArtist object or None'''
    try:
        return MBArtist.objects.get(name=artist_name)
    except MBArtist.DoesNotExist:
        return None

def lookup_artist(artist, logger):
    '''Looks up Artist locally or in musicbrainz and asssociates Artist object
    with MBArtist.'''
    logger.debug(artist.name + " ...")
    mb_artist = get_local_mb_artist(artist.name)
    if mb_artist:
        artist.mb_artist_id = mb_artist.mb_id
        artist.name = mb_artist.name
        artist.save()
    else:
        name_filter = ws.ArtistFilter(name=artist.name, limit=5)
        q = ws.Query()
        artist_results = call_mb_ws(q.getArtists, name_filter)
        time.sleep(settings.SLEEP_TIME)
        if artist_results:
            mb_artist_name = artist_results[0].artist.name
            mb_artist_id = artist_results[0].artist.id
            artist.mb_artist_id = mb_artist_id
            artist.name = mb_artist_name
            artist.save()
            mb_artist, created = MBArtist.objects.get_or_create(mb_id=mb_artist_id, name=mb_artist_name)
            if created:
                mb_artist.fetch_albums()

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

def get_releases(album_name, mb_artist_id):
    release_filter = ws.ReleaseFilter(
                            title=album_name,
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
            if '503' in e.message:
                logger.debug('function ' + function.func_name + ' failed with 503, sleeping ' + str(settings.SLEEP_TIME * i) + ' seconds')
                time.sleep(settings.SLEEP_TIME * i)
                i *= 2
            else:
                raise e
 
