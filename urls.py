import os.path

from django.views.generic.simple import direct_to_template
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'library.views.upload', name="home"),
    url(r'^library/', include('library.urls'), name="library"),
    url(r'^privacy/$', direct_to_template, {'template': 'library/privacy_policy.html'}, name="privacy"),
    url(r'^api/', include('api.urls'), name="api"),
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^assets/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.dirname(__file__), 'assets')}),
    )
