#!/usr/bin/env python
import plistlib
import logging

from django.conf import settings

from library.models import *
from library import signals

logging.basicConfig(filename=settings.LOG_FILE, level=logging.INFO)

class LibraryImporter:
    def itunes(self, sender, **kwargs):
        logging.info("Starting import...")
        itunes = plistlib.readPlist(kwargs['file'])
        tracks = itunes["Tracks"]
        library = Library(name=kwargs['name'])
        library.save()
        for track in tracks.values():
            if track.get("Artist") and track.get("Album"):
                logging.info(track["Artist"] + " - " + track["Album"])
                artist, created = library.artist_set.get_or_create(name=track["Artist"])
                artist.album_set.get_or_create(name=track["Album"])
                if track.get("Play Count"):
                    artist.play_count += track["Play Count"]
                    artist.save()
        library.processing = False
        library.save()
        
        # signals.import_done.send(sender=self, library=library)
