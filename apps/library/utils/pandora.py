import urllib
from lxml import etree
from sets import Set

namespaces = { 'pandora': "http://www.pandora.com/rss/1.0/modules/pandora/",
               'sy': "http://purl.org/rss/1.0/modules/syndication/",
               'content': "http://purl.org/rss/1.0/modules/content/",
               'dc': "http://purl.org/dc/elements/1.1/",
               'mm': "http://musicbrainz.org/mm/mm-2.1#",
               'fh': "http://purl.org/syndication/history/1.0",
               'itms': "http://phobos.apple.com/rss/1.0/modules/itms/",
               'az': "http://www.amazon.com/gp/aws/landing.html",
               'xsi': "http://www.w3.org/2001/XMLSchema-instance" }

def fetch_artists(username):
    '''Fetches set of artist names from pandora for user 'username'.

    Uses station rss feed and the song and artist bookmark feeds.

    '''
    url = 'http://feeds.pandora.com/feeds/people/%s/favorites.xml' % username
    tree = etree.fromstring(urllib.urlopen(url).read())
    artist_elements = tree.xpath('//mm:Artist/dc:title/text()', 
                                 namespaces=namespaces)
    artists = Set([str(element) for element in artist_elements])
    
    url = 'http://feeds.pandora.com/feeds/people/%s/stations.xml' % username
    tree = etree.fromstring(urllib.urlopen(url).read())
    artist_elements = tree.xpath('//pandora:artist/text()',
                                 namespaces=namespaces)
    artists.update([str(element) for element in artist_elements])

    url = 'http://feeds.pandora.com/feeds/people/%s/favoriteartists.xml' \
        % username
    tree = etree.fromstring(urllib.urlopen(url).read())
    artist_elements = tree.xpath('//mm:Artist/dc:title/text()', 
                                 namespaces=namespaces)
    artists.update([str(element) for element in artist_elements])
    return artists
