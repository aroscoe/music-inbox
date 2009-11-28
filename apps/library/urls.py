from django.conf.urls.defaults import *

from library.views import Library, libraries_resource

library = Library(permitted_methods=('GET','POST'))

urlpatterns = patterns('',
    url(r'^test/(.*?)/?$', libraries_resource),
    url(r'^upload/?$', library.create),
    url(r'^(.*?)/?$', library),
)