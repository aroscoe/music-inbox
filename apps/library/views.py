from django.http import HttpResponse
from django.http import Http404
from django.utils import simplejson as json

from rest.django_restapi.resource import Resource
from rest.django_restapi.model_resource import Collection
from rest.django_restapi.responder import JSONResponder

from library.models import *

libraries_resource = Collection(
    queryset = Library.objects.all(),
    responder = JSONResponder()
)

class Library(Resource):
    def read(self, request, library_id):
        artists = Artist.objects.filter(library=library_id).select_related('album')
        if artists:
            response = {}
            for artist in artists:
                albums = artist.album_set.all()
                response[artist.name] = list(albums.values_list('name', flat=True))
            return HttpResponse(json.dumps(response), mimetype='application/json')
        else:
            return Http404