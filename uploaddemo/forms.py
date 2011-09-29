from django import forms

from uploaddemo.models import Upload

class UploadForm(forms.models.ModelForm):
    class Meta:
        model = Upload
        exclude = ('uploaded_by', 'timestamp')
