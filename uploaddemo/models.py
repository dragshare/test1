import datetime
import os

from django.conf import settings
from django.core.files import storage
from django.db import models
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _

class FileSystemStorage(storage.FileSystemStorage):
    """
    Subclass Django's standard FileSystemStorage to fix permissions
    of uploaded files.
    """
    def _save(self, name, content):
       name =  super(FileSystemStorage, self)._save(name, content)
       full_path = self.path(name)
       mode = getattr(settings, 'FILE_UPLOAD_PERMISSIONS', None)
       if not mode:
           mode = 0644
       os.chmod(full_path, mode)
       return name

class Upload(models.Model):
    """Uploaded files."""
    file = models.FileField(storage=FileSystemStorage(location=settings.MEDIA_ROOT), upload_to='uploads', help_text=_(u"""The file itself."""))
    timestamp = models.DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        ordering = ['-timestamp',]
    
    def __unicode__(self):
        return u"%s" % (self.file)
    
    @property
    def size(self):
        return filesizeformat(self.file.size)
