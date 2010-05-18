from django.conf.urls.defaults import *

from api.views import LibraryResource, libraries_resource, missing

library = LibraryResource(permitted_methods=('GET','POST'))

urlpatterns = patterns('',
    # Example of using django_restapi
    url(r'^test/(.*?)/?$', libraries_resource),
    
    # Library
    url(r'^library/upload/?$', library.create, name="api_library_upload"),
    url(r'^library/(\d+)/missing/?$', missing, name="api_library_missing"),
    url(r'^library/(.*?)/?$', library, name="api_library"),
)
