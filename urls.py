from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

import os.path

import django_cron

admin.autodiscover()

django_cron.autodiscover()

urlpatterns = patterns('',
    (r'^api/', include('api.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^library/', include('library.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^assets/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.dirname(__file__), 'assets')}),
    )
