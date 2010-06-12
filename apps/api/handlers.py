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
            
class MissingLibraryHandler(LibraryHandler):
    allowed_methods = ('GET')
    fields = ('processing', 'missing_albums')
    
    @classmethod
    def missing_albums(cls, library):
        return library.missing_albums_dict()

# TODO: must be a way to merge this with LibraryHandler.create
# TODO: what's a better name for this?
class LibraryFormHandler(BaseHandler):
    model = Library
    allowed_methods = ('POST')
    
    def create(self, request):
        library_id = LibraryView().post_form_data(request)
        if library_id:
            return {'rssUri': utils.rss_url(library_id)}
        else:
            return {'error': 'library name missing'}
