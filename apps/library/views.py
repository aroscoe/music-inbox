import uuid
import logging

from django.http import Http404
from django.conf import settings
from django.shortcuts import redirect
from django.views.generic.simple import direct_to_template
from django.contrib.sites.models import Site

from library.models import Library, Artist
from library.forms import *
from library.utils import decrypt_id, encrypt_id
from library.tasks import import_itunes_file

logging.basicConfig(filename=settings.LOG_FILE)
logger = logging.getLogger("library_views")
logger.setLevel(settings.LOG_LEVEL)

class LibraryView:

    def post_library(self, request):
        logger.debug("posted")
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            logger.debug("valid")
            library_name = form.cleaned_data['name']
            
            library = Library(name=library_name)
            library.save()
            
            library_filename = self._save_library_file(request.FILES['file'])
            
            import_itunes_file.delay(library.id, library_filename)
            
            return library, None
        return None, form
    
    def _save_library_file(self, file):
        guid = uuid.uuid4().get_hex()
        file_path = settings.UPLOADS_DIR + guid + ".xml"
        destination = open(file_path, 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
        return file_path

def upload(request):
    if request.method == 'POST':
        library, form = LibraryView().post_library(request)
        if library:
            library_id = encrypt_id(library.pk)
            return redirect('library_success', library_id=library_id)
    else:
        form = UploadFileForm()
    return direct_to_template(request, 'library/upload.html', locals())

def library(request, library_id):
    try:
        library = Library.objects.get(pk=decrypt_id(library_id, Http404))
    except Library.DoesNotExist:
        raise Http404
    albums = library.albums_dict()
    return direct_to_template(request, 'library/library.html', locals())

def success(request, library_id):
    try:
        library = Library.objects.get(pk=decrypt_id(library_id, Http404))
    except Library.DoesNotExist:
        raise Http404
    site_domain = Site.objects.get_current().domain
    return direct_to_template(request, 'library/success.html', locals())

