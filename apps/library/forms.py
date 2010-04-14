from django import forms

class UploadFileForm(forms.Form):
    name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'txtbox'}))
    file = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn_browse'}))
    
    def clean_file(self):
        file = self.cleaned_data['file']
        if file.content_type != 'text/xml':
            raise forms.ValidationError("Wrong file type. Please choose another file.")
        return file