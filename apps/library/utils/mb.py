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
        logger.debug(artist.name + " ...")
        name_filter = ws.ArtistFilter(name=artist.name, limit=5)
        q = ws.Query()
        artist_results = q.getArtists(name_filter) # TODO aliases if no albums match
        time.sleep(1)
        if artist_results:
            mb_artist_id = artist_results[0].artist.id
            artist.mb_artist_id = mb_artist_id
            artist.save()
            
            local_release_group_ids = set([get_release_group_id(release_group, mb_artist_id) for release_group in artist.album_set.all()])
            mb_artist_entry, created_artist = MBArtist.objects.get_or_create(mb_id=mb_artist_id)
            if created_artist:
                mb_artist_entry.name = artist.name
                mb_artist_entry.save()
            
                mb_artist_entry.fetch_albums()
                
def get_artist_id(artist_name):
    name_filter = ws.ArtistFilter(name=artist_name, limit=5)
    q = ws.Query()
    return q.getArtists(name_filter)[0].artist.id

def get_release_group_id(album, mb_artist_id):
    releases = get_releases(album.name, mb_artist_id)
    time.sleep(1)
    if releases:
            includes = ws.ReleaseIncludes(releaseGroup=True)
            q = ws.Query()
            id = q.getReleaseById(releases[0].release.id, includes).releaseGroup.id
            time.sleep(1)
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
    return q.getReleases(release_filter)
