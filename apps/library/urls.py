from django.conf.urls.defaults import *
from library.feed import NewAlbums
from django.contrib.syndication.views import feed as feedview

feeds = {'newalbums': NewAlbums}

urlpatterns = patterns('library.views',
    url(r'^$', 'upload', name="library_home"),

    # RSS Feed
    url(r'^feeds/(?P<url>.*)/$', feedview, {'feed_dict': feeds}),

    # catch all pattern at the end
    url(r'^(.*?)/?$', 'library', name="library"),
)

