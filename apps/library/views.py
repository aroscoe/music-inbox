from django.conf import settings
from django.views.generic.simple import direct_to_template
from library.models import Library as LibraryModel
from library.forms import *
from library import signals
import threading

class LibraryView:
    def upload(self, request): #TODO: abstract the upload code into its own lib so that the api and internal library app can use it (the remove unnecessary Class)
        if request.method == 'POST':
            library = self.post_library(request)
            if library:
                return direct_to_template(request, 'library/success.html', locals())
        else:
            form = UploadFileForm()
        return direct_to_template(request, 'library/upload.html', locals())
    
    def post_library(self, request):
        print "posted"
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print "valid"
            library_name = form.cleaned_data['name']
            library_file = self._handle_uploaded_file(request.FILES['file'])
            
            # Create Library to send along with the signal and send pk back in the response
            library = LibraryModel(name=library_name)
            library.save()
            
            t = threading.Thread(target=signals.upload_done.send, kwargs={'sender': self, 'file': library_file, 'library': library})
            t.setDaemon(True)
            t.start()
            return library
        return None

    
    def _handle_uploaded_file(self, file):
        file_path = settings.UPLOADS_DIR + file.name
        destination = open(file_path, 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
        return file_path
