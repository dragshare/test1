import datetime
import time
import logging
import mimetypes
import os.path

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.forms.models import save_instance
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _

from uploaddemo.forms import UploadForm
from uploaddemo.models import Upload

@staff_member_required
def confirm_delete(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    
    upload = get_object_or_404(Upload, id=request.POST.get('id', None))
    data = {
        'upload': upload
    }
    return render_to_response('confirm_delete.html', data, RequestContext(request))

@staff_member_required
def delete(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    
    if request.POST.get('delete', False):
        upload = get_object_or_404(Upload, id=request.POST.get('id', None))
        upload.delete()
        request.user.message_set.create(message=_('The file has been deleted.'))

    return HttpResponseRedirect(reverse('uploads'))

def list(request):
    data = {
        'form': UploadForm(),
        'uploads': Upload.objects.all()
    }
    return render_to_response('list.html', data, RequestContext(request))

@staff_member_required
def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            logging.info("Upload form is valid: %s" % form)
            upload = Upload()
            upload.uploaded_by = request.user
            upload.timestamp = datetime.datetime.now()
            
            save_instance(form, upload)
            logging.info("Saved upload: %s" % upload)
            request.user.message_set.create(message=_('Your file has been received.'))
        else:
            logging.error("invalid form: %s" % form)
            logging.error("form errors: %s" % form.errors)

    return HttpResponseRedirect(reverse('uploads'))

@staff_member_required
def upload_progress(request):
    """
    Return JSON object with information about the progress of an upload.
    """
    if 'HTTP_X_PROGRESS_ID' in request.META:
        progress_id = request.META['HTTP_X_PROGRESS_ID']
        from django.utils import simplejson
        cache_key = "%s_%s" % (request.META['REMOTE_ADDR'], progress_id)
        data = cache.get(cache_key)
        json = simplejson.dumps(data)
        print '---------'
        print cache_key
        print data
        return HttpResponse(json)
    else:
        logging.error("Received progress report request without X-Progress-ID header. request.META: %s" % request.META)
        return HttpResponseBadRequest('Server Error: You must provide X-Progress-ID header or query param.')


