import logging

from celery.decorators import task
from django.conf import settings
import plistlib

from library.models import *
from library import signals


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
    
    # TODO not sure if this still makes sense, should probably just trigger
    # another task
    #signals.import_done.send(sender=None, library=library)
