from django.conf.urls.defaults import *

from api.views import LibraryResource, libraries_resource, missing
from library.feed import NewAlbums

library = LibraryResource(permitted_methods=('GET','POST'))

feeds = {'newalbums': NewAlbums}

urlpatterns = patterns('',
    # Example of using django_restapi
    url(r'^test/(.*?)/?$', libraries_resource),
    
    # Library
    url(r'^library/upload/?$', library.create),
    url(r'^library/(\d+)/missing/?$', missing),
    url(r'^library/(.*?)/?$', library),
    
    # RSS Feed
    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
)
