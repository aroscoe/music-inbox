from django.conf.urls.defaults import *

from library.views import *

urlpatterns = patterns('',
    url(r'^upload/', upload),
    url(r'^(\d+)/', Library()),
    url(r'^test/(.*?)/?$', libraries_resource),
)