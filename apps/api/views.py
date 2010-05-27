from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.utils import simplejson as json
from django.shortcuts import render_to_response
from django.conf import settings

from rest.django_restapi.resource import Resource
from rest.django_restapi.model_resource import Collection
from rest.django_restapi.responder import JSONResponder
from data_responder import JSONDataResponder

from library.models import Artist
from library.models import Library
from library.forms import *
from library.views import LibraryView
from library import utils

libraries_resource = Collection(
    queryset = Library.objects.all(),
    responder = JSONResponder()
)

class LibraryResource(Resource):
    def read(self, request, library_id):
        try:
            library = Library.objects.get(pk=utils.decrypt_id(library_id, 
                                                                   Library.DoesNotExist))
        except Library.DoesNotExist:
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
                responder = JSONDataResponder({'upload_success': 'true', 'library_id': str(utils.encrypt_id(library.pk))})
            else:
                # Create real dict from form.errors (ErrorDict)
                errors = dict([(k, [unicode(e) for e in v]) for k,v in form.errors.items()])
                responder = JSONDataResponder({'upload_success': 'false', 'errors': errors})
            return responder.response

    def handle_form_data(self, request):
        '''Handles post request of form data for library imports'''
        if request.method == 'POST':
            library_id = LibraryView().post_form_data(request)
            if library_id:
                data = {'rssUri': utils.rss_url(library_id)}
            else:
                data = {'error': 'library name missing'}
            return HttpResponse(json.dumps(data, 'utf-8'), 
                                mimetype='application/json; charset=utf-8')
        else:
            return HttpResponseBadRequest('POST expected')
    
def missing(request, library_id):
    try:
        library = Library.objects.get(pk=utils.decrypt_id(library_id, 
                                                          Library.DoesNotExist))
    except Library.DoesNotExist:
        raise Http404
    
    response = {}
    missing_albums = library.missing_albums_dict()
    for mb_artist, missing_mb_albums in missing_albums.iteritems():
        response[mb_artist.name] = [album.name for album in missing_mb_albums]
    
    responder = JSONDataResponder(response)
    if library.processing: responder.processing = 2
    return responder.response
