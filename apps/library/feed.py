from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.syndication.feeds import FeedDoesNotExist
from django.contrib.syndication.feeds import Feed
from django.contrib.sites.models import Site

from library.models import *
from library import utils

class FirstItem(object):
    '''
    Feed item that is displayed to users if there are no items in their
    NewAlbums feed yet. For this purpose, the FirstItem has to have the fields
    an actual feed item has.
    '''
    amazon_url = "http://%s/" % Site.objects.get_current().domain
    release_date = datetime.now()
    title = 'Music Inbox: No new albums available yet'
    description = '''You successfully installed your personal music inbox feed.

In the future, you will be notified about new releases from your favorite artists
here.
'''
    def __init__(self, library_id):
        self.amazon_url = utils.rss_url(library_id) 


class NewAlbums(Feed):

    title_template = "library/feed_item_title.html"
    description_template = "library/feed_item_description.html"
    
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Library.objects.get(id=utils.decrypt_id(bits[0], ObjectDoesNotExist))
    
    def title(self, obj):
        if obj.name:
            return "New albums for %s" % obj.name
        else:
            return "New albums"

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return obj.url()

    def description(self, obj):
        if obj.name:
            return "New albums for artists in %s's library" % obj.name
        else:
            return "New albums for artists in your library"

    def items(self, obj):
        albums = obj.missing_albums()
        if not albums:
            return [FirstItem(obj.id)]
        else:
            albums = [album for album in albums if album.amazon_url and album.release_date and album.release_date <= datetime.now()]
            return albums[:10]

    def item_link(self, item):
        if item.amazon_url: 
            return item.amazon_url
        else:
            return "%s.html" % item.mb_id

    def item_pubdate(self, item):
        if item.release_date:
            return datetime(item.release_date.year, item.release_date.month, item.release_date.day)
        else:
            # return datetime.now()
            # return datetime(1970, 1, 1)
            return None
