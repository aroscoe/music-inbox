from django.conf.urls.defaults import *

from piston.resource import Resource

from api.views import LibraryResource, libraries_resource, missing
from api.handlers import LibraryHandler, MissingLibraryHandler

library = LibraryResource(permitted_methods=('GET','POST'))

piston_library = Resource(handler=LibraryHandler)
piston_form_library = Resource(handler=LibraryFormHandler)
piston_missing_library = Resource(handler=MissingLibraryHandler)

urlpatterns = patterns('',
    # Example of using django_restapi
    url(r'^test/(.*?)/?$', libraries_resource),
    
    # Piston
    url(r'^piston-library/form/?$', piston_form_library, name="piston-api_library_form"),
    url(r'^piston-library/(\d+)/missing/?$', piston_missing_library, name="piston-api_library_missing"),
    url(r'^piston-library/?$', piston_library, name="piston-api_library_upload"),
    url(r'^piston-library/(?P<library_id>[^/]+)/', piston_library, name="piston-api_library"),
    
    # Library
    url(r'^library/upload/?$', library.create, name="api_library_upload"),
    url(r'^library/(\d+)/missing/?$', missing, name="api_library_missing"),
    url(r'^library/form/?$', library.handle_form_data),
    url(r'^library/(.*?)/?$', library, name="api_library"),
)
