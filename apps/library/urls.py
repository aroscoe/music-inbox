from django.conf.urls.defaults import *

from library.views import *

urlpatterns = patterns('',
    url(r'^(\d+)/', library, name="library"),
    url(r'^test/(.*?)/?$', libraries_resource, name="library_all"),
)