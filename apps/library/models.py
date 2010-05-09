import sys
import time
import logging
import fcntl
from datetime import date

from django.conf import settings
from django.db import models
from django.contrib.sites.models import Site

import musicbrainz2.webservice as ws
import musicbrainz2.model as m

from library import utils

logging.basicConfig()
logger = logging.getLogger("models")
logger.setLevel(settings.LOG_LEVEL)

try:
    from settings import AMAZON_KEY, AMAZON_SECRET, AMAZON_ASSOCIATE_TAG
    amazon_enabled = True
except ImportError:
    logger.debug("amazon search disabled")
    amazon_enabled = False

class Library(models.Model):
    name = models.CharField(max_length=60, blank=True)
    processing = models.BooleanField(default=1)
    
    def __str__(self):
        return self.name

    def url(self):
        return 'http://%s/library/%s/' % \
            (Site.objects.get_current().domain, utils.encrypt_id(self.id))

    def url_link(self):
        return '<a target="_blank" href="%s">%s</a>' % (self.url(), self.url())
    url_link.allow_tags = True
    
    def missing_albums_dict(self):
        """return a dictionary of MBArtist to a list of MBAlbum, only containing missing albums"""
        response = {}
        artists = self.artist_set.all()
        if artists:
            for artist in artists:
                if artist.mb_artist_id:
                    mb_artist = MBArtist.objects.get(mb_id=artist.mb_artist_id)
                    mb_album_ids = set([album.mb_id for album in mb_artist.mbalbum_set.all()])
                    has_album_ids = set([album.mb_id for album in artist.album_set.all()])
                    missing_album_ids = mb_album_ids - has_album_ids
                    if missing_album_ids:
                        missing_albums = []
                        for album_id in missing_album_ids:
                            missing_albums.append(MBAlbum.objects.get(mb_id=album_id))
                        response[MBArtist.objects.get(mb_id=artist.mb_artist_id)] = missing_albums
        
        return response
    
    def _newest_(self, album1, album2):
        if not album1.release_date and not album2.release_date:
            return -sys.maxint # arbitrary
        if not album1.release_date:
            return sys.maxint
        if not album2.release_date:
            return -sys.maxint
        return -1 * cmp(album1.release_date, album2.release_date)
    
    def albums_dict(self):
        """return a dictionary of Albums with the key being Artist"""
        response = {}
        artists = self.artist_set.all().select_related()
        if artists:
            for artist in artists:
                response[artist.name] = list(artist.album_set.values_list('name', flat=True))
        return response
    
    def missing_albums(self):
        """return a list of missing MBAlbums in order of release date or sort_function if that is specified"""
        missing_albums_d = self.missing_albums_dict()
        missing_albums_list = []
        for albums in missing_albums_d.values():
            missing_albums_list.extend(albums)
        return sorted(missing_albums_list, self._newest_)
    
    class Meta:
        verbose_name_plural = 'libraries'
    
    class Admin:
        pass

class Artist(models.Model):
    name = models.CharField(max_length=200)
    library = models.ForeignKey(Library)
    mb_artist_id = models.CharField(max_length=150)
    play_count = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name
    
    def __unicode__(self):
        return u'%s' % (self.name)
    
    class Admin:
        pass
    
class MBArtist(models.Model):
    mb_id = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=150)
    
    def __str__(self):
        return self.name
    
    def __unicode__(self):
        return u'%s' % (self.name)
    
    def fetch_albums(self, logger):
        include = ws.ArtistIncludes(
                releases=(m.Release.TYPE_OFFICIAL, m.Release.TYPE_ALBUM), 
                tags=True, releaseGroups=True)
        q = ws.Query()
        # artist query including their releases
        try:
            mb_artist = call_mb_ws(q.getArtistById, logger, self.mb_id,
                                   include)
            for release in mb_artist.getReleaseGroups():
                mb_album, created_album = MBAlbum.objects.get_or_create(mb_id=release.id, artist = self)
                if created_album:
                    logger.debug(release.title + " ...")
                    # query
                    date, asin = self.get_release_date(release.id, logger)
                    mb_album.release_date = date
                    mb_album.name = release.title
                    if asin:
                        mb_album.asin = asin
                    if amazon_enabled:
                        # amazon query
                        mb_album.amazon_url = search_on_amazon(asin, release.title, self.name)
                    mb_album.save()
        except ws.WebServiceError, e:
            logger.debug('q.getArtistById failed for ' + self.mb_id)
    
    def get_release_date(self, release_group_id, logger):
        includes = ws.ReleaseGroupIncludes(releases=True)
        q = ws.Query()
        try:
            release_group = call_mb_ws(q.getReleaseGroupById, logger, 
                                       release_group_id, includes)
            time.sleep(settings.SLEEP_TIME)
            if release_group and release_group.releases:
                release = release_group.releases[0] # TODO iterate over all
                includes = ws.ReleaseIncludes(releaseEvents = True)
                release = call_mb_ws(q.getReleaseById, logger, release.id, 
                                     includes)
                time.sleep(settings.SLEEP_TIME)
                release_date = release.getEarliestReleaseDate()
                if release_date:
                    logger.debug("   " + release_date)
                    month = 1
                    day = 1
                    parsed_release_date = release_date.split('-')
                    year = int(parsed_release_date[0])
                    if len(parsed_release_date) > 1:
                        month = int(parsed_release_date[1])
                    if len(parsed_release_date) > 2:
                        day = int(parsed_release_date[2])
                    return date(year, month, day), release.asin
            return None, None
        except ws.WebServiceError, e:
            return None, None
    
    class Admin:
        pass

class Album(models.Model):
    name   = models.CharField(max_length=150)
    artist = models.ForeignKey(Artist)
    mb_id = models.CharField(max_length=150)
    
    def __str__(self):
        return '%s - %s' % (self.artist.name, self.name)
    
    #def __unicode__(self):
    #    return u'%s - %s' % (self.artist.name, self.name)
    
    class Admin:
        pass

class MBAlbum(models.Model):
    mb_id  = models.CharField(max_length=150, unique=True)
    name   = models.CharField(max_length=150)
    release_date = models.DateField(null=True)
    artist = models.ForeignKey(MBArtist)
    asin = models.CharField(max_length=40, blank=True)
    amazon_url = models.URLField(verify_exists=False, max_length=500, blank=True)
    
    def __str__(self):
        return '%s - %s' % (self.artist.name, self.name)
    
    def __unicode__(self):
        return u'%s - %s' % (self.artist.name, self.name)
    
    class Admin:
        pass

def search_on_amazon(asin, album, artist):
    '''
    Tries to locate the url of album by artis on amazon
    
    Returns '' if it can't be found
    '''
    from amazonproduct import API
    
    if not AMAZON_KEY or not AMAZON_SECRET or not AMAZON_ASSOCIATE_TAG:
        return ''
    
    api = API(AMAZON_KEY, AMAZON_SECRET, 'us')
    try:
        if asin:
            node = api.item_lookup(asin, AssociateTag=AMAZON_ASSOCIATE_TAG)
            for item in node.Items:
                attributes = item.Item.ItemAttributes
                if attributes.ProductGroup == 'Music':
                    url = item.Item.DetailPageURL
                    if url:
                        return url.text
        node = api.item_search('MP3Downloads', Keywords=album + ' ' + artist, AssociateTag=AMAZON_ASSOCIATE_TAG)
        for item in node.Items:
            attributes = item.Item.ItemAttributes
            if attributes.Creator == artist and attributes.Title == album and attributes.ProductGroup == 'Digital Music Album':
                url = item.Item.DetailPageURL
                if url:
                    return url.text
    except :
        pass
    return ''

def album_diff(library, logger):
    logger.debug("processing " + library.name + " ...")
    
    for artist in library.artist_set.order_by("-play_count"):
        lookup_artist(artist, logger)

def get_local_mb_artist(artist_name):
    '''Returns local MBArtist object or None'''
    try:
        return MBArtist.objects.get(name=artist_name)
    except MBArtist.DoesNotExist:
        return None

def lookup_artist(artist, logger):
    '''Looks up Artist locally or in musicbrainz and asssociates Artist object
    with MBArtist.'''
    logger.debug(artist.name + " ...")
    mb_artist = get_local_mb_artist(artist.name)
    if mb_artist:
        artist.mb_artist_id = mb_artist.mb_id
        artist.name = mb_artist.name
        artist.save()
    else:
        name_filter = ws.ArtistFilter(name=artist.name, limit=5)
        q = ws.Query()
        artist_results = call_mb_ws(q.getArtists, logger, name_filter)
        time.sleep(settings.SLEEP_TIME)
        if artist_results:
            mb_artist_name = artist_results[0].artist.name
            mb_artist_id = artist_results[0].artist.id
            artist.mb_artist_id = mb_artist_id
            artist.name = mb_artist_name
            artist.save()
            mb_artist, created = MBArtist.objects.get_or_create(mb_id=mb_artist_id, name=mb_artist_name)
            if created:
                mb_artist.fetch_albums(logger)

def call_mb_ws(function, logger, *args):
    i = 1
    lock = open(settings.MEDIA_ROOT + '/lock', 'w')
    while True:
        try:
            fcntl.lockf(lock, fcntl.LOCK_EX)
            result = function(*args)
            time.sleep(settings.SLEEP_TIME)
            return result
        except ws.WebServiceError, e:
            if '503' in e.message:
                logger.debug('function ' + function.func_name + ' failed with 503, sleeping ' + str(settings.SLEEP_TIME * i) + ' seconds')
                time.sleep(settings.SLEEP_TIME * i)
                i *= 2
            else:
                raise e
        finally:
            fcntl.lockf(lock, fcntl.LOCK_UN)
 
