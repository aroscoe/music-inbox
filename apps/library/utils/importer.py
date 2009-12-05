#!/usr/bin/env python
import plistlib

from library.models import *
from library import signals

class LibraryImporter:
    def itunes(self, sender, **kwargs):
        itunes = plistlib.readPlist(kwargs['file'])
        tracks = itunes["Tracks"]
        library = Library(name=kwargs['name'])
        library.save()
        for track in tracks.values():
            if track.get("Artist") and track.get("Album"):
                artist,created = library.artist_set.get_or_create(name=track["Artist"])
                artist.album_set.get_or_create(name=track["Album"])
                if track.get("Play Count"):
                    artist.play_count += track["Play Count"]
                    artist.save()
        signals.import_done.send(sender=self, library=library)
