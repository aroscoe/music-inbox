import logging
import plistlib

from django.conf import settings
from celery.decorators import task

from library.models import *
from library.utils.mb import album_diff

@task
def import_itunes_file(library_id, library_filename, **kwargs):
    '''Reads itunes xml file and extracs artists and albums from its tracks.
    
    Saves artist and tracks to database as part of the library.
    
    '''
    logger = import_itunes_file.get_logger(**kwargs)
    
    logger.debug("reading file %s for library %s" 
                 % (library_filename, library_id))
    
    library = Library.objects.get(pk=library_id)
    
    itunes = plistlib.readPlist(library_filename)
    tracks = itunes["Tracks"]
    
    for track in tracks.values():
        if track.get("Artist") and track.get("Album"):
            artist, created = library.artist_set.get_or_create(name=track["Artist"])
            artist.album_set.get_or_create(name=track["Album"])
            if track.get("Play Count"):
                artist.play_count += track["Play Count"]
                artist.save()
    library.processing = False
    library.save()
    
    diff_albums.delay(library_id)

@task
def diff_albums(library_id, **kwargs):
    ''' '''
    logger = diff_albums.get_logger(**kwargs)
    logger.debug("diffing albums of library %s" % library_id)
    
    library = Library.objects.get(pk=library_id)
    
    album_diff(library, logger)

