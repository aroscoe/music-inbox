from django import forms

class UploadFileForm(forms.Form):
    name = forms.CharField(max_length=150)
    file = forms.FileField()
