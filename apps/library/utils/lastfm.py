from django.conf import settings

import pylast

lastfm = pylast.get_lastfm_network(settings.LASTFM_API_KEY, settings.LASTFM_API_SECRET)