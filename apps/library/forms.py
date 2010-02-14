from django import forms

class UploadFileForm(forms.Form):
    name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'txtbox'}))
    file = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn_browse'}))
