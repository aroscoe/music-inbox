from django.contrib import admin

from library.models import *

class AlbumAdmin(admin.ModelAdmin):
    list_display = ('artist', 'name')

admin.site.register(Library)
admin.site.register(Artist)
admin.site.register(Album, AlbumAdmin)
