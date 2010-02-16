from django.conf.urls.defaults import *

urlpatterns = patterns('library.views',
    url(r'^$', 'upload', name="library_home"),
    url(r'^(.*?)/?$', 'library', name="library"),
    url(r'^/amazon/(.*?)/$', 'library', name='amazon'),
)

