from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

import os.path

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^itunes-inbox/', include('itunes-inbox.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^assets/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.dirname(__file__), 'assets')}),
    )