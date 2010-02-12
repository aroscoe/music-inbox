from django.contrib import admin

from api.models import *

class AlbumAdmin(admin.ModelAdmin):
    list_display = ('artist', 'name')

admin.site.register(Library)
#admin.site.register(MissingLibrary)
admin.site.register(Artist)
admin.site.register(Album, AlbumAdmin)
admin.site.register(MBArtist)
admin.site.register(MBAlbum)
