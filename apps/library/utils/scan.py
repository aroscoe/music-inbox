from library import models

def scan_all_artists():
    '''Iterates through all Artist objects and checks whether their mb_id
    points to a valid MBArtist.
    
    '''
    artists = models.Artist.objects.all()
    for artist in artists:
        if artist.mb_artist_id:
            print artist
            models.MBArtist.object.get(mb_id=artist.mb_artist_id)

def scan_all_albums():
    '''Iterates over all Album objects and checks whether their mb_id
    points to a valid MBAlbum.

    '''
    albums = models.Album.objects.all()
    for album in albums:
        if album.mb_id:
            print album
            models.MBAlbum.object.get(mb_id=album.mb_id)