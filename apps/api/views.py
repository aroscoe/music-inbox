from django.http import HttpResponse, Http404
from django.utils import simplejson as json
from django.shortcuts import render_to_response
from django.conf import settings

from rest.django_restapi.resource import Resource
from rest.django_restapi.model_resource import Collection
from rest.django_restapi.responder import JSONResponder
from data_responder import JSONDataResponder

from library.models import Artist
from library.models import Library as LibraryModel
from library.forms import *
from library.views import LibraryView
from library.utils import decrypt_id, encrypt_id

libraries_resource = Collection(
    queryset = LibraryModel.objects.all(),
    responder = JSONResponder()
)

class LibraryResource(Resource):
    def read(self, request, library_id):
        try:
            library = LibraryModel.objects.get(pk=decrypt_id(library_id, LibraryModel.DoesNotExist))
        except LibraryModel.DoesNotExist:
            raise Http404
        albums = library.albums_dict()
        responder = JSONDataResponder(albums)
        if library.processing: responder.processing = 2
        return responder.response
    
    # Example cURL POST
    # curl -H "Content-Type: multipart/form-data" -F "file=@test_library.xml" -F "name=Anthony" http://localhost:8000/library/
    def create(self, request, *args):
        if request.method == 'POST':
            library, form = LibraryView().post_library(request)
            if library:
                responder = JSONDataResponder({'library_id': encrypt_id(library.pk)})
                return responder.response

def missing(request, library_id):
    try:
        library = LibraryModel.objects.get(pk=decrypt_id(library_id, LibraryModel.DoesNotExist))
    except LibraryModel.DoesNotExist:
        raise Http404
    
    response = {}
    missing_albums = library.missing_albums_dict()
    for mb_artist, missing_mb_albums in missing_albums.iteritems():
        response[mb_artist.name] = [album.name for album in missing_mb_albums]
    
    responder = JSONDataResponder(response)
    if library.processing: responder.processing = 2
    return responder.response
