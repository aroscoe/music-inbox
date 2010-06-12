from django.conf.urls.defaults import *

from piston.resource import Resource

# from api.views import LibraryResource, libraries_resource, missing
from api.handlers import LibraryHandler, LibraryFormHandler, MissingLibraryHandler

# library = LibraryResource(permitted_methods=('GET','POST'))

library = Resource(handler=LibraryHandler)
library_form = Resource(handler=LibraryFormHandler)
missing_library = Resource(handler=MissingLibraryHandler)

urlpatterns = patterns('',
    url(r'^library/form/?$', library_form, name="api_library_form"),
    url(r'^library/(\d+)/missing/?$', missing_library, name="api_library_missing"),
    url(r'^library/?$', library, name="api_library_upload"),
    url(r'^library/(?P<library_id>[^/]+)/', library, name="api_library"),
    
    # Example of using django_restapi
    # url(r'^test/(.*?)/?$', libraries_resource),
    
    # Library
    # url(r'^library/upload/?$', library.create, name="api_library_upload"),
    # url(r'^library/(\d+)/missing/?$', missing, name="api_library_missing"),
    # url(r'^library/form/?$', library.handle_form_data),
    # url(r'^library/(.*?)/?$', library, name="api_library"),
)
