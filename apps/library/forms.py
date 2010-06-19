import re

from django import forms

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
        count = 1
        pattern = '<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">'
        for line in file:
            if re.match(pattern, line):
                return True
            else:
                if count < 4:
                    count += 1
                else:
                    break
        return False