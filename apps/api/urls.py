from django.conf.urls.defaults import *

from piston.resource import Resource

from api.views import LibraryResource, libraries_resource, missing
from api.handlers import LibraryHandler

library = LibraryResource(permitted_methods=('GET','POST'))
piston_library = Resource(handler=LibraryHandler)

urlpatterns = patterns('',
    # Example of using django_restapi
    url(r'^test/(.*?)/?$', libraries_resource),
    
    # Piston
    url(r'^piston-library/?$', piston_library, name="piston-api_library"),
    url(r'^piston-library/(?P<library_id>[^/]+)/', piston_library, name="piston-api_library"),
    
    # Library
    url(r'^library/upload/?$', library.create, name="api_library_upload"),
    url(r'^library/(\d+)/missing/?$', missing, name="api_library_missing"),
    url(r'^library/form/?$', library.handle_form_data),
    url(r'^library/(.*?)/?$', library, name="api_library"),
)
