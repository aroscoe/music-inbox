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
            mb_artist = q.getArtistById(artist_results[0].artist.id, include)
            for release in mb_artist.getReleases():
                found = False
                for local_album in artist.album_set.all():
                    if(local_album.name == release.title):
                        found = True
                        break
                if not found:
                    temp_artist.album_set.get_or_create(name=release.title)
    return missing

    