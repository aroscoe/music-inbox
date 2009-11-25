import musicbrainz2.webservice as ws
import musicbrainz2.model as m

from library.models import *

def album_diff(sender, **kwargs):
    library = kwargs['library']
    missing = Library.objects.get_or_create(name=library.name + "_missing")[0]
    for artist in library.artist_set.all():
        temp_artist = missing.artist_set.get_or_create(name=artist.name)[0]
        name_filter = ws.ArtistFilter(name=artist.name, limit=5)
        q = ws.Query()
        artist_results = q.getArtists(name_filter)
        if artist_results:
            include = ws.ArtistIncludes(
                releases=(m.Release.TYPE_OFFICIAL, m.Release.TYPE_ALBUM), tags=True, releaseGroups=True)
            mb_artist_id = artist_results[0].artist.id
            mb_artist = q.getArtistById(mb_artist_id, include)
            mb_release_group_ids = set([release_group.id for release_group in mb_artist.getReleaseGroups()])
            local_release_group_ids = set([get_release_group_id(release_group.name, mb_artist_id) for release_group in artist.album_set.all()])
            missing_album_group_ids = mb_release_group_ids - local_release_group_ids
            for release in mb_artist.getReleaseGroups():
                if(release.id in missing_album_group_ids):
                    temp_artist.album_set.get_or_create(name=release.title)     
    return missing
                
def get_artist_id(artist_name):
    name_filter = ws.ArtistFilter(name=artist_name, limit=5)
    q = ws.Query()
    return q.getArtists(name_filter)[0].artist.id

def get_release_group_id(album_name, mb_artist_id):
    releases = get_releases(album_name, mb_artist_id)
    if releases:
            includes = ws.ReleaseIncludes(releaseGroup=True)
            q = ws.Query()
            return q.getReleaseById(releases[0].release.id, includes).releaseGroup.id
    return None

def get_releases(name, mb_artist_id):
    release_filter = ws.ReleaseFilter(
                            title=name,
                            artistId=mb_artist_id,
                            releaseTypes=(m.Release.TYPE_OFFICIAL,
                                    m.Release.TYPE_ALBUM))
    q = ws.Query()
    return q.getReleases(release_filter)


