import random
import tempfile
import os
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django import forms

temp_storage = FileSystemStorage(tempfile.mkdtemp())

# Write out a file to be used as default content
temp_storage.save('tests/default.txt', ContentFile('default content'));

class FileModel(models.Model):
    def random_upload_to(self, filename):
        return '%s/%s' % (random.randint(100, 999), filename)

    testfile = models.FileField(storage=temp_storage, upload_to='test_upload')
    random = models.FileField(storage=temp_storage, upload_to=random_upload_to)

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
