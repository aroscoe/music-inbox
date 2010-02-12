from django.conf.urls.defaults import *

urlpatterns = patterns('demo.views',
    url(r'^$', 'upload', name="demo_home"),
)