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
                releases=(m.Release.TYPE_OFFICIAL, m.Release.TYPE_ALBUM), tags=True, releaseGroups=True)
            mb_artist_id = artist_results[0].artist.id
            mb_artist = q.getArtistById(mb_artist_id, include)
            for release_group in mb_artist.getReleaseGroups():
                found = False
                for local_album in artist.album_set.all():
                    # if(local_album.name == release.title):
                    if(same_album(local_album.name, release_group, mb_artist_id)):
                        found = True
                        break
                if not found:
                    temp_artist.album_set.get_or_create(name=release_group.title)
    return missing

def same_album(local_album_name, mb_release_group, mb_artist_id):
        return getReleaseGroupID(local_album_name, mb_artist_id) == mb_release_group.id

def _same_album(local_album_name, mb_release_group, mb_artist_id):
        release_group_filter = ws.ReleaseGroupFilter(
                                title=local_album_name,
                                artistId=mb_artist_id,
                                releaseTypes=(m.Release.TYPE_OFFICIAL,
                                        m.Release.TYPE_ALBUM))
        q = ws.Query()
        releases_with_local_name = q.getReleaseGroups(release_group_filter)
        if releases_with_local_name:
                if releases_with_local_name[0].release.asin and mb_release_group.asin:
                        return mb_release_group.asin == releases_with_local_name[0].releaseGroup.asin
                else:
                        return mb_release_group.title == local_album_name
                # TODO when releaseGroup ids are populated
                # return mb_release_group.id == releases_with_local_name[0].releaseGroup.id
        return False
                
def getArtistID(artist_name):
        name_filter = ws.ArtistFilter(name=artist_name, limit=5)
        q = ws.Query()
        return q.getArtists(name_filter)[0].artist.id

def getReleaseGroupID(album_name, mb_artist_id):
        releases = getReleases(album_name, mb_artist_id)
        if releases:
                includes = ws.ReleaseIncludes(releaseGroup=True)
                q = ws.Query()
                return q.getReleaseById(releases[0].release.id, includes).releaseGroup.id
        #release_group_filter = ws.ReleaseGroupFilter(
        #                        title=album_name,
        #                        artistId=mb_artist_id,
        #                        releaseTypes=(m.Release.TYPE_OFFICIAL,
        #                                m.Release.TYPE_ALBUM))
        #q = ws.Query()
        #return q.getReleaseGroups(release_group_filter)
        return None
        
def getReleases(name, mb_artist_id):
        release_filter = ws.ReleaseFilter(
                                title=name,
                                artistId=mb_artist_id,
                                releaseTypes=(m.Release.TYPE_OFFICIAL,
                                        m.Release.TYPE_ALBUM))
        q = ws.Query()
        return q.getReleases(release_filter)
        
    