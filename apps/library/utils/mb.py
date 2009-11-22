import musicbrainz2.webservice as ws
import musicbrainz2.model as m

from library.models import *

def album_diff(library):
    missing = Library.objects.get_or_create(name=library.name + "_missing")[0]
    for artist in library.artist_set.all():
        temp_artist = missing.artist_set.get_or_create(name=artist.name)[0]
        name_filter = ws.ArtistFilter(name=artist.name, limit=5)
        q = ws.Query()
        artist_results = q.getArtists(name_filter)
        if artist_results:
            include = ws.ArtistIncludes(
                releases=(m.Release.TYPE_OFFICIAL, m.Release.TYPE_ALBUM), tags=True)
            mb_artist_id = artist_results[0].artist.id
            mb_artist = q.getArtistById(mb_artist_id, include)
            for release in mb_artist.getReleases():
                found = False
                for local_album in artist.album_set.all():
                    # if(local_album.name == release.title):
                    if(same_album(local_album.name, release, mb_artist_id)):
                        found = True
                        break
                if not found:
                    temp_artist.album_set.get_or_create(name=release.title)
    return missing

def same_album(local_album_name, mb_release, mb_artist_id):
        release_filter = ws.ReleaseFilter(
                                title=local_album_name,
                                artistId=mb_artist_id,
                                releaseTypes=(m.Release.TYPE_OFFICIAL,
                                        m.Release.TYPE_ALBUM))
        q = ws.Query()
        releases_with_local_name = q.getReleases(release_filter)
        if releases_with_local_name:
                return mb_release.id == releases_with_local_name[0].release.id
        return False
                
def getArtistID(artist_name):
        name_filter = ws.ArtistFilter(name=artist_name, limit=5)
        q = ws.Query()
        return q.getArtists(name_filter)[0].artist.id

def getAlbum(name, mb_artist_id):
        release_filter = ws.ReleaseFilter(
                                title=name,
                                artistId=mb_artist_id,
                                releaseTypes=(m.Release.TYPE_OFFICIAL,
                                        m.Release.TYPE_ALBUM))
        q = ws.Query()
        return q.getReleases(release_filter)
        
    