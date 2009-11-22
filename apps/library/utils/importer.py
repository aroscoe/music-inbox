#!/usr/bin/env python

import plistlib

from library.models import *

def itunes(file, name):
    itunes = plistlib.readPlist(file)
    tracks = itunes["Tracks"]
    library = Library(name=name)
    library.save()
    for track in tracks.values():
        if track.get("Artist") and track.get("Album"):
            artist,created = library.artist_set.get_or_create(name=track["Artist"])
            artist.album_set.get_or_create(name=track["Album"])

if __name__ == "__main__":
    itunes_import(sys.argv[1,2])