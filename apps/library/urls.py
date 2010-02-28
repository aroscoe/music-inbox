from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from library.feed import NewAlbums
from django.contrib.syndication.views import feed as feedview

feeds = {'newalbums': NewAlbums}

urlpatterns = patterns('library.views',
    url(r'^$', 'upload', name="library_home"),
    url(r'^privacy/$', direct_to_template,
        { 'template': 'library/privacy_policy.html' }),

    # RSS Feed
    url(r'^feeds/(?P<url>.*)/$', feedview, {'feed_dict': feeds}),

    # catch all pattern at the end
    url(r'^(.*?)/?$', 'library', name="library"),
)

