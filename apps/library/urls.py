from django.conf.urls.defaults import *
from library.views import LibraryView

lv = LibraryView()

urlpatterns = patterns('',
    url(r'^$', lv.upload, name="library_home"),
)

