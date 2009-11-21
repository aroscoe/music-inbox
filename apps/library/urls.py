from django.conf.urls.defaults import *

from library.views import *

urlpatterns = patterns('',
    url(r'^(\d+)/', Library()),
    url(r'^test/(.*?)/?$', libraries_resource),
)