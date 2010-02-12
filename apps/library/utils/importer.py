#!/usr/bin/env python
import plistlib
import logging

from django.conf import settings

from library.models import *
from library import signals

class LibraryImporter:
    def itunes(self, sender, **kwargs):
        itunes = plistlib.readPlist(kwargs['file'])
        tracks = itunes["Tracks"]
        library = kwargs['library']
        for track in tracks.values():
            if track.get("Artist") and track.get("Album"):
                artist, created = library.artist_set.get_or_create(name=track["Artist"])
                artist.album_set.get_or_create(name=track["Album"])
                if track.get("Play Count"):
                    artist.play_count += track["Play Count"]
                    artist.save()
        library.processing = False
        library.save()
        
        signals.import_done.send(sender=self, library=library)
