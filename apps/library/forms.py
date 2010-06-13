import re

from django import forms

class UploadFileForm(forms.Form):
    name = forms.CharField(required=False, max_length=150)
    file = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn_browse'}))
    
    def clean_file(self):
        file = self.cleaned_data['file']
        valid_content_types = ['text/xml', 'application/xml', 'application/octet-stream']
        
        # Check file has correct content type
        if file.content_type in valid_content_types:
            
            # Read first few lines of file to double check file is what it's content type says it is
            max_lines = 4
            count = 1
            pattern = '<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">'
            for line in file:
                if re.match(pattern, line):
                    break
                else:
                    if count < 4:
                        count += 1
                    else:
                        raise forms.ValidationError("Wrong file type. Please choose another file.")
                        break
        else:
            raise forms.ValidationError("Wrong file type. Please choose another file.")
        
        return file