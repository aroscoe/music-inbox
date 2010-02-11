from django.db import models

import musicbrainz2.webservice as ws
import musicbrainz2.model as m
import time
from datetime import date

class Library(models.Model):
    name = models.CharField(max_length=60, blank=True)
    processing = models.BooleanField(default=1)
    
    def __str__(self):
        return self.name
    
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
    
    def _newest_(album1, album2):
        return -1 * cmp(album1.release_date, album2.release_date)
    
    def missing_albums(self, sort_function=_newest_):
        """return a list of missing MBAlbums in order of release date or sort_function if that is specified"""
        missing_albums_d = self.missing_albums_dict()
        missing_albums_list = []
        for albums in missing_albums_d.values():
            missing_albums_list.extend(albums)
        return sorted(missing_albums_list, sort_function)
    
    class Meta:
        verbose_name_plural = 'libraries'
    
    class Admin:
        pass

class Artist(models.Model):
    name = models.CharField(max_length=150)
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
    
    def fetch_albums(self):
        include = ws.ArtistIncludes(
                releases=(m.Release.TYPE_OFFICIAL, m.Release.TYPE_ALBUM), tags=True, releaseGroups=True)
        q = ws.Query()
        mb_artist = q.getArtistById(self.mb_id, include)
        time.sleep(1)
        for release in mb_artist.getReleaseGroups():
            mb_album, created_album = MBAlbum.objects.get_or_create(mb_id=release.id, artist = self)
            if created_album:
                print release.title + " ..."
                date, asin = self.get_release_date(release.id)
                mb_album.release_date = date
                mb_album.name = release.title
                mb_album.amazon_url = search_on_amazon(asin, release.title, self.name)
                mb_album.save()

    def get_release_date(self, release_group_id):
        includes = ws.ReleaseGroupIncludes(releases=True)
        q = ws.Query()
        release_group = q.getReleaseGroupById(release_group_id, includes)
        time.sleep(1)
        if release_group:
            release = release_group.releases[0] # TODO iterate over all
            includes = ws.ReleaseIncludes(releaseEvents = True)
            release = q.getReleaseById(release.id, includes)
            time.sleep(1)
            release_date = release.getEarliestReleaseDate()
            if release_date:
                print "   " + release_date
                month = 1
                day = 1
                parsed_release_date = release_date.split('-')
                year = int(parsed_release_date[0])
                if len(parsed_release_date) > 1:
                    month = int(parsed_release_date[1])
                if len(parsed_release_date) > 2:
                    day = int(parsed_release_date[2])
                return date(year, month, day), release.asin
        return None, release.asin

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
    from settings import AMAZON_KEY, AMAZON_SECRET
    from amazonproduct import API

    if not AMAZON_KEY or not AMAZON_SECRET:
        return ''
    
    api = API(AMAZON_KEY, AMAZON_SECRET, 'us')
    try:
        if asin:
            node = api.item_lookup(asin)
            for item in node.Items:
                attributes = item.Item.ItemAttributes
                if attributes.ProductGroup == 'Music':
                    url = item.Item.DetailPageURL
                    if url:
                        return url.text
        node = api.item_search('MP3Downloads', Keywords=album + ' ' + artist)
        for item in node.Items:
            attributes = item.Item.ItemAttributes
            if attributes.Creator == artist and attributes.Title == album and attributes.ProductGroup == 'Digital Music Album':
                url = item.Item.DetailPageURL
                if url:
                    return url.text
    except :
        pass
    return ''


#################################################################
# Library Signal Handling

from library import signals
from library.utils.importer import LibraryImporter
from library.utils.mb import album_diff

library_importer = LibraryImporter()
signals.upload_done.connect(library_importer.itunes)

signals.import_done.connect(album_diff)
