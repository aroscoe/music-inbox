from django.conf import settings

import pylast

lastfm = pylast.get_lastfm_network(settings.LASTFM_API_KEY, settings.LASTFM_API_SECRET)

def get_artists(user, limit=None, min_playcount=None):
    library = user.get_library()
    artists = library.get_artists(limit=limit)
    if min_playcount:
        artists = [artist for artist in artists if artist.playcount >= min_playcount]
    return artists

    