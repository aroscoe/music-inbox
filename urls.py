from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

import os.path

admin.autodiscover()

urlpatterns = patterns('',
    (r'^library/', include('library.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^demo/', include('demo.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^assets/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.dirname(__file__), 'assets')}),
    )
