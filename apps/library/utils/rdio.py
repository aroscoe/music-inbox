from django.conf import settings
from rdioapi import Rdio

def create_rdio():
    state = {}
    return Rdio(settings.RDIO_CONSUMER_KEY, settings.RDIO_SECRET, state)
    
def get_user(username):
    r = create_rdio();
    return r.findUser(vanityName=username)

def fetch_artists(username):
    user = get_user(username)
    r = create_rdio();
    return [artist['name'] for artist in r.getArtistsInCollection(user=user['key'])]
