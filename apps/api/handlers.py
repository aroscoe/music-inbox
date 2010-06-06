from piston.handler import BaseHandler

from library.models import Library
from library.views import LibraryView
from library import utils

class LibraryHandler(BaseHandler):
    model = Library
    allowed_methods = ('GET', 'POST')
    fields = ('processing', 'albums')
    
    def read(self, request, library_id):
        library_id = utils.decrypt_id(library_id, '')
        return super(LibraryHandler, self).read(request, id=library_id)
    
    @classmethod
    def albums(cls, library):
        return library.albums_dict()
    
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