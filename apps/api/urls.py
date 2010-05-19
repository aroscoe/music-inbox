from django.conf.urls.defaults import *

from api.views import LibraryResource, libraries_resource, missing

library = LibraryResource(permitted_methods=('GET','POST'))

urlpatterns = patterns('',
    # Example of using django_restapi
    url(r'^test/(.*?)/?$', libraries_resource),
    
    # Library
    url(r'^library/upload/?$', library.create),
    url(r'^json/?$', library.upload_json),
    url(r'^library/(\d+)/missing/?$', missing),
    url(r'^library/(.*?)/?$', library),
)
