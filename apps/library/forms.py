from django import forms

class UploadFileForm(forms.Form):
    name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'txtbox required'}))
    file = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn_browse'}))
    
    # TODO: Come up with new validation for file upload. Curl sends the file with 
    # application/xml and swfupload sends application/octet-stream
    
    # def clean_file(self):
    #     file = self.cleaned_data['file']
    #     if file.content_type != 'text/xml':
    #         raise forms.ValidationError("Wrong file type. Please choose another file.")
    #     return file