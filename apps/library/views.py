import logging

from django.http import Http404
from django.conf import settings
from django.views.generic.simple import direct_to_template

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
            
            # Create Library to send along with the signal and send id back in
            # the response
            library = Library(name=library_name)
            library.save()

            library_filename = self._save_library_file(request.FILES['file'], 
                                                       library.id)
            
            import_itunes_file.delay(library.id, library_filename)
            
            return library
        return None
    
    def _save_library_file(self, file, library_id):
        file_path = settings.UPLOADS_DIR + str(library_id) + ".xml"
        destination = open(file_path, 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
        return file_path

def upload(request):
    if request.method == 'POST':
        library = LibraryView().post_library(request)
        if library:
            library_id = encrypt_id(library.pk)
            return direct_to_template(request, 'library/success.html', locals())
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

