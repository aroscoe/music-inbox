from django.core.exceptions import ObjectDoesNotExist
from django.contrib.syndication.feeds import FeedDoesNotExist
from django.contrib.syndication.feeds import Feed
from library.models import *
from datetime import datetime

class NewAlbums(Feed):

    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Library.objects.get(id=bits[0])
    
    def title(self, obj):
        return "New albums for %s" % obj.name

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        #return obj.get_absolute_url()
        return "%s" % obj.id

    def description(self, obj):
        return "New albums for artists in %s's library" % obj.name

    def items(self, obj):
        return obj.missing_albums()[:10]

    def item_link(self, obj):
        return "%s.html" % obj.mb_id

    def item_pubdate(self, obj):
        return datetime(obj.release_date.year, obj.release_date.month, obj.release_date.day)
