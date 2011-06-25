import uuid
import logging
import zlib

from django.http import Http404
from django.conf import settings
from django.shortcuts import redirect
from django.views.generic.simple import direct_to_template
from django.contrib.sites.models import Site

from library.models import Library, Artist, MBAlbum
from library import forms
from library import utils
from library import tasks

logging.basicConfig(filename=settings.LOG_FILE)
logger = logging.getLogger("library_views")
logger.setLevel(settings.LOG_LEVEL)

class LibraryView:
    
    def post_library(self, request):
        form = forms.UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            library_name = form.cleaned_data.get('name', None)
            if library_name == None:
                library = Library()
            else:
                library = Library(name=library_name)
            library.save()
            
            library_filename = self._save_library_file(request.FILES['file'])
            
            tasks.import_itunes_file.delay(library.id, library_filename)
            
            return library, None
        return None, form
    
    def post_form_data(self, request):
        '''
        Accepts an 'application/x-www-form-urlencoded' post request with 
        key-value pairs of artist=album and a name=name of library pair
        
        '''
        logger.debug('form posted')
        data = request.POST
        if 'name' in data:
            library_name = data['name']
            library = Library(name=library_name)
        else:
            library = Library()
        library.save()
        tasks.import_form_data.delay(library.pk, data)
        return library.pk
        # TODO: validate data is in correct format
        # logger.debug('posted data invalid %s' % data)
        # return None
    
    def _save_library_file(self, file):
        guid = uuid.uuid4().get_hex()
        file_path = settings.UPLOADS_DIR + guid + ".xml"
        decompressor = zlib.decompressobj()
        destination = open(file_path, 'wb')
        for chunk in file.chunks():
            destination.write(decompressor.decompress(chunk))
        destination.write(decompressor.flush())
        destination.close()
        return file_path

def upload(request):
    if request.method == 'POST':
        library, form = LibraryView().post_library(request)
        if library:
            library_id = utils.encrypt_id(library.pk)
            return redirect('library_success', library_id=library_id)
    else:
        recent_albums = MBAlbum.objects.order_by('-release_date').select_related()[:10]
        recent_albums = [album for album in recent_albums if album.amazon_url]
        recent_albums = recent_albums[:min(len(recent_albums), 5)]
        form = forms.UploadFileForm()
    return direct_to_template(request, 'library/upload.html', locals())

def library(request, library_id):
    try:
        library = Library.objects.get(pk=utils.decrypt_id(library_id, Http404))
    except Library.DoesNotExist:
        raise Http404
    albums = library.albums_dict()
    return direct_to_template(request, 'library/library.html', locals())

def success(request, library_id):
    try:
        library = Library.objects.get(pk=utils.decrypt_id(library_id, Http404))
    except Library.DoesNotExist:
        raise Http404
    return direct_to_template(request, 'library/success.html', locals())

def pandora_import(request):
    '''Handles post request of pandora username for artists import from
    pandora.

    '''
    form = forms.PandoraUsernameForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        library = Library(name=username)
        library.save()
        tasks.import_pandora_artists.delay(library.id, username)
        library_id = utils.encrypt_id(library.pk)
        return redirect('library_success', library_id)
    else:
        form = forms.PandoraUsernameForm()
        return direct_to_template(request, 'library/upload.html', locals())

def lastfm_import(request):
    '''Handles post request of last.fm username for artists import from
    last.fm.

    '''
    if request.method == 'POST':
        form = forms.LastfmUsernameForm(request.POST)
        if form.is_valid():
            user = form.user
            library = Library(name=user.name)
            library.save()
            tasks.import_lastfm_artists.delay(library.id, user)
            library_id = utils.encrypt_id(library.pk)
            return redirect('library_success', library_id)
    else:
        form = forms.LastfmUsernameForm()
    return direct_to_template(request, 'test_form.html', {'form': form})

def rdio_import(request):
    '''Handles post request of rdio username for artists import from
    rdio.

    '''
    form = forms.RdioUsernameForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        library = Library(name=username)
        library.save()
        tasks.import_rdio_artists.delay(library.id, username)
        library_id = utils.encrypt_id(library.pk)
        return redirect('library_success', library_id)
    else:
        form = forms.RdioUsernameForm()
    return direct_to_template(request, 'library/upload.html', locals())
