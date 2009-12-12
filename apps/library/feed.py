from django.core.exceptions import ObjectDoesNotExist
from django.contrib.syndication.feeds import *
from library.models import *

class feed(Feed):

    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Library.objects.get(id=bits[0])
    
    def title(self, obj):
        return "New albums for %s" % lib.name

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return "/newalbums/%s" % obj.id
    
    def description(self, obj):
        return "New albums for artists in %s's library" % lib.name

    def items(self, obj):
        return lib.missing_albums()
