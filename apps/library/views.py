from django.http import HttpResponse, Http404
from django.utils import simplejson as json
from django.shortcuts import render_to_response
from django.conf import settings

from rest.django_restapi.resource import Resource
from rest.django_restapi.model_resource import Collection
from rest.django_restapi.responder import JSONResponder
from data_responder import JSONDataResponder

from library.models import *
from library.forms import *

libraries_resource = Collection(
    queryset = Library.objects.all(),
    responder = JSONResponder()
)

class Library(Resource):
    def read(self, request, library_id):
        artists = Artist.objects.filter(library=library_id).select_related()
        if artists:
            data = {}
            for artist in artists:
                albums = artist.album_set.all()
                data[artist.name] = list(albums.values_list('name', flat=True))
            
            responder = JSONDataResponder(data)
            if artist.library.processing: responder.processing = 2
            return responder.response
        else:
            return Http404
    
    # Example cURL POST
    # curl -H "Content-Type: multipart/form-data" -F "file=@test_library.xml" -F "name=Anthony" http://localhost:8000/library/
    def create(self, request, *args):
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                library_name = form.cleaned_data['name']
                library_file = self._handle_uploaded_file(request.FILES['file'])
                signals.upload_done.send(sender=self, file=library_file, name=library_name)
                return render_to_response('success.html')
        else:
            form = UploadFileForm()
        return render_to_response('upload.html', {'form': form})
    
    def _handle_uploaded_file(self, file):
        file_path = settings.UPLOADS_DIR + file.name
        destination = open(file_path, 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
        return file_path

def missing(request, library_id):
    artists = Artist.objects.filter(library=library_id)
    if artists:
        response = {}
        for artist in artists:
            print artist.name
            if artist.mb_artist_id:
                print artist.mb_artist_id
                mb_artist = MBArtist.objects.get(mb_id=artist.mb_artist_id)
                mb_album_ids = set([album.mb_id for album in mb_artist.mbalbum_set.all()])
                has_album_ids = set([album.mb_id for album in artist.album_set.all()])
                missing_album_ids = mb_album_ids - has_album_ids
                response[artist.name] = []
                for mb_album in mb_artist.mbalbum_set.all():
                    print mb_album.name
                    if mb_album.mb_id in missing_album_ids:
                        response[artist.name].append(mb_album.name)
        return HttpResponse(json.dumps(response), mimetype='application/json')
    else:
        return Http404

    
