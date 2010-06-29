from django.conf.urls.defaults import *
from django.contrib.syndication.views import feed as feedview

from library.feed import NewAlbums

feeds = {'newalbums': NewAlbums}

urlpatterns = patterns('library.views',
    url(r'^$', 'upload', name="library_home"),
    url(r'^pandora/?$', 'pandora_import', name='pandora_import'),
    url(r'^lastfm/?$', 'lastfm_import', name='library_lastfm_import'),
    url(r'^success/(\d+)/?$', 'success', name="library_success"),

    # RSS Feed
    url(r'^feeds/(?P<url>.*)/$', feedview, {'feed_dict': feeds}),

    # catch all pattern at the end
    url(r'^(.*?)/?$', 'library', name="library"),
)

