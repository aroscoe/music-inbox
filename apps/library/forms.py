import re
import zlib

from django import forms
from django.conf import settings

from library.utils.lastfm import lastfm

class UploadFileForm(forms.Form):
    name = forms.CharField(required=False, max_length=150)
    file = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn_browse'}))
    
    def clean_file(self):
        file = self.cleaned_data['file']
        if not self.validate_file_content_type(file) or not self.validate_file_contents(file):
            raise forms.ValidationError("Wrong file type. Please choose another file.")
        return file
    
    def validate_file_content_type(self, file):
        """Validate a file's content type with the one expected."""
        valid_content_types = ['text/xml', 'application/xml', 'application/octet-stream']
        if file.content_type in valid_content_types:
            return True
        return False
    
    def validate_file_contents(self, file):
        """Read first few lines of a file checking for a specific pattern."""
        max_lines = 4
        pattern = '<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">'
        data = zlib.decompress(file.read())
        lines = data.split('\n')
        for count, line in enumerate(lines):
            if pattern in line:
                return True
            if count > 4:
                break
        return False

class PandoraUsernameForm(forms.Form):
    username = forms.CharField(max_length=150)

class LastfmUsernameForm(forms.Form):
    username = forms.CharField(max_length=150)
    
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = lastfm.get_user(username)
            user.get_id()
        except:
            raise forms.ValidationError("User doesn't exist.")
        self.user = user
        return username