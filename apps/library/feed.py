from django.core.exceptions import ObjectDoesNotExist
from django.contrib.syndication.feeds import FeedDoesNotExist
from django.contrib.syndication.feeds import Feed
from library.models import *
from datetime import datetime

from settings import AMAZON_KEY, AMAZON_SECRET
from amazonproduct import API

class NewAlbums(Feed):

    api = API(AMAZON_KEY, AMAZON_SECRET)

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
        amazon_link = search_on_amazon(obj.name, obj.artist.name)
        if amazon_link:
            return amazon_link
        else:
            return "%s.html" % obj.mb_id

    def item_pubdate(self, obj):
        return datetime(obj.release_date.year, obj.release_date.month, obj.release_date.day)


    def search_on_amazon(album, artist):
        try:
            node = api.item_search('MP3Downloads', Keywords=album + ' ' + artist)
            for item in node.Items:
                attributes = item.Item.ItemAttributes
                if attributes.Creator == artist and attributes.Title == album
                and attributes.ProductGroup == 'Digital Music Album':
                return item.Item.DetailPageURL
        except:
            return None
        
