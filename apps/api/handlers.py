from piston.handler import BaseHandler
from piston.utils import rc

from library.models import Library
from library.views import LibraryView
from library import utils

class LibraryHandler(BaseHandler):
    allowed_methods = ('GET', 'POST')
    model = Library
    
    def read(self, request, library_id):
        try:
            library = Library.objects.get(pk=utils.decrypt_id(library_id, Library.DoesNotExist))
        except Library.DoesNotExist:
            return rc.NOT_HERE
        albums = library.albums_dict()
        processing = 2 if library.processing else 1
        return {'processing': processing, 'data': albums}
    
    # Example cURL POST
    # curl -H "Content-Type: multipart/form-data" -F "file=@test_library.xml" -F "name=Anthony" http://localhost:8000/api/piston-library/
    def create(self, request, *args):
        library, form = LibraryView().post_library(request)
        if library:
            return {'upload_success': 'true', 'library_id': str(utils.encrypt_id(library.pk))}
        else:
            # Create real dict from form.errors (ErrorDict)
            errors = dict([(k, [unicode(e) for e in v]) for k,v in form.errors.items()])
            return {'upload_success': 'false', 'errors': errors}
