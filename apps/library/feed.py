from django.core.exceptions import ObjectDoesNotExist
from django.contrib.syndication.feeds import FeedDoesNotExist
from django.contrib.syndication.feeds import Feed
from library.models import *
from datetime import datetime

from library.utils import decrypt_id, encrypt_id

class FirstItem(object):
    amazon_url = "http://musicinbox.org/"
    release_date = datetime.now()
    title = 'Music Inbox: No new albums available yet'
    description = '''You successfully installed your personal music inbox feed.

In the future, you will be notified about new albums from your favorite artists
here.
'''

class NewAlbums(Feed):

    title_template = "library/feed_item_title.html"
    description_template = "library/feed_item_description.html"

    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Library.objects.get(id=decrypt_id(bits[0], ObjectDoesNotExist))
    
    def title(self, obj):
        return "New albums for %s" % obj.name

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        #return obj.get_absolute_url()
        return "%s" % encrypt_id(obj.id, KEY)

    def description(self, obj):
        return "New albums for artists in %s's library" % obj.name

    def items(self, obj):
        albums = obj.missing_albums()[:10]
        if not albums:
            return [FirstItem()]
        else:
            return albums

    def item_link(self, item):
        if item.amazon_url: 
            return item.amazon_url
        else:
            return "%s.html" % item.mb_id

    def item_pubdate(self, item):
        return datetime(item.release_date.year, item.release_date.month, item.release_date.day)
