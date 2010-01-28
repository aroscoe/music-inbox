from django.conf.urls.defaults import *

from library.views import LibraryResource, libraries_resource, missing
from library.feed import NewAlbums

library = LibraryResource(permitted_methods=('GET','POST'))

feeds = {'newalbums': NewAlbums}

urlpatterns = patterns('',
    url(r'^test/(.*?)/?$', libraries_resource),
    url(r'^upload/?$', library.create),
    url(r'^(\d+)/missing/?$', missing),
    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    url(r'^(.*?)/?$', library),
)
