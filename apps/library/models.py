from django.db import models

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

    def __str__(self):
        return '%s - %s' % (self.artist.name, self.name)

    def __unicode__(self):
        return u'%s - %s' % (self.artist.name, self.name)

    class Admin:
        pass


#################################################################
# Library Signal Handling

from library import signals
from library.utils.importer import LibraryImporter
from library.utils.mb import album_diff

library_importer = LibraryImporter()
signals.upload_done.connect(library_importer.itunes)

signals.import_done.connect(album_diff)
