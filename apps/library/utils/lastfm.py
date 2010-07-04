from django.conf import settings

import pylast

lastfm = pylast.get_lastfm_network(settings.LASTFM_API_KEY, settings.LASTFM_API_SECRET)

def get_artists(user, limit=None, min_playcount=None):
    library = user.get_library()
    artists = library.get_artists(limit=limit)
    if min_playcount:
        artists = [artist for artist in artists if artist.playcount >= min_playcount]
    return artists

def get_albums(user, limit=None):
    # FIXME: Bad Data - The Decemberists: [u'The Decemberists - The Hazards Of Love (Album)']
    library = user.get_library()
    albums = library.get_albums(limit=limit)
    albums_dict = {}
    for album in albums:
        if albums_dict.get(album.item.artist.name):
            albums_dict[album.item.artist.name].append(album.item.title)
        else:
            albums_dict[album.item.artist.name] = [album.item.title]
    return albums_dict

def get_library(user, artist_limit=None, album_limit=None, min_playcount=None):
    # FIXME: Bad Data - Arcade Fire from get_artists, The Arcade Fire from get_albums
    artists = get_artists(user, artist_limit, min_playcount=4)
    albums = get_albums(user, album_limit)
    library = {}
    for artist in artists:
        library[artist.item.name] = {'playcount': artist.playcount, 'albums': albums.get(artist.item.name)}
    return library