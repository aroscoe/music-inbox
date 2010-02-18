from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('library.views',
    url(r'^$', 'upload', name="library_home"),
    (r'^privacy/$', direct_to_template,
     { 'template': 'library/privacy_policy.html' }),
    url(r'^(.*?)/?$', 'library', name="library"),
)

