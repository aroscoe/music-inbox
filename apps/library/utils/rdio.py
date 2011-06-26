from django.conf import settings
from rdioapi import Rdio

def get_user(username):
    state = {}
    r = Rdio(settings.RDIO_CONSUMER_KEY, settings.RDIO_SECRET, state)
    return r.findUser(vanityName=username)

def fetch_artists(username):
    user = get_user(user_name)
    return [artist['name'] for artist in r.getArtistsInCollection(user=user['key'])]
