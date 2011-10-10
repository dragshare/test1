import os
from django.core.files.uploadedfile import UploadedFile
from django.http import HttpResponse, HttpResponseServerError, HttpResponseRedirect, HttpResponseBadRequest
from django.utils.hashcompat import sha_constructor
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils import simplejson 
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.core.cache import cache

#@csrf_exempt
def index(request):
    return render_to_response('index.html', RequestContext(request))

#@csrf_exempt
def file_upload(request):
    """
    Check that a file upload can be updated into the POST dictionary without
    going pear-shaped.
    """

    if request.method == 'POST':
        print 'upload file -------------'
        print len(request.FILES)
        upfile = request.FILES['upfile']
        user = request.user.username
        print 'upload file name =========='
        print upfile.name
        try:
            destfile = "/tmp/django/" + user + "/" + upfile.name
            dest = open(destfile, 'wb+')
            for chunk in upfile.chunks():
                dest.write(chunk)
            dest.close()
        except:
            return HttpResponse('fail to upload')
    else:
        return HttpResponse('Please use POST')

    return HttpResponseRedirect(reverse('index'))


def upload_progress(request):
    """
    Return JSON object with information about the progress of an upload.
    """
    progress_id = ''
    if 'X-Progress-ID' in request.GET:
        progress_id = request.GET['X-Progress-ID']
    if 'HTTP_X_PROGRESS_ID' in request.META:
        progress_id = request.META['HTTP_X_PROGRESS_ID']

    if progress_id:
        from django.utils import simplejson
        cache_key = "%s_%s" % (request.META['REMOTE_ADDR'], progress_id)
        data = cache.get(cache_key)
        json = simplejson.dumps(data)
        return HttpResponse(json)
    else:
        return HttpResponseBadRequest('Server Error: You must provide X-Progress-ID header or query param.')


#@csrf_exempt
def file_list(request):
    """
    List all files belonged to one user
    """

    tags = []

    if request.method == 'GET':
        user = request.user.username
        if request.GET.has_key('tag_list_name'):
            tag_list_name = request.GET['tag_list_name']
            dest_dir = '/tmp/django/'
            if user is None:
                dest_dir += user + '/'
            dest_dir += tag_list_name
            try: 
                 tags = os.listdir(dest_dir)
            except:
                return HttpResponse('fail to list')
        else:
            return HttpResponse('Please specify tag list name')
    else:
        return HttpResponse('Please use GET')

    return render_to_response('index.html', {'tag_list': tags}, RequestContext(request))


def file_read(request):
    """
    Read one file content
    """

    fcontent = ''

    if request.method == 'GET':
        user = request.user.username
        if request.GET.has_key('file_name'):
            file_name = request.GET['file_name']
            dest_file = '/tmp/django/'
            if user is None:
                dest_file += user + '/'
            dest_file += file_name
            try: 
                 fd = open(dest_file, 'r')
                 # read one page
                 fcontent = fd.read(4096)
                 fd.close()
            except:
                return HttpResponse('fail to read')
        else:
            return HttpResponse('Please specify file name')
    else:
        return HttpResponse('Please use GET')

    return render_to_response('index.html', {'file_content': fcontent}, RequestContext(request))


def file_thumb(request):
    """
    Give a thumb of one file content
    """

    return HttpResponse()

