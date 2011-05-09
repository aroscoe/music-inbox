from settings import RDIO_CONSUMER_KEY, RDIO_SECRET
from rdioapi import Rdio

def get_user(username):
    state = {}
    r = Rdio(RDIO_CONSUMER_KEY, RDIO_SECRET, state)
    return r.findUser(vanityName=username)

def fetch_artists(username):
    user = get_user(user_name)
    return [artist['name'] for artist in r.getArtistsInCollection(user=user['key'])]
