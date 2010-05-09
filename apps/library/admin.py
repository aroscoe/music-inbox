from django.contrib import admin

from library.models import *

class LibraryAdmin(admin.ModelAdmin):
    list_display = ('name', 'processing', 'url_link')

class AlbumAdmin(admin.ModelAdmin):
    list_display = ('artist', 'name')

admin.site.register(Library, LibraryAdmin)
#admin.site.register(MissingLibrary)
admin.site.register(Artist)
admin.site.register(Album, AlbumAdmin)
admin.site.register(MBArtist)
admin.site.register(MBAlbum)
