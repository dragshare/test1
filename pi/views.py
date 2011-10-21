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

def response_mimetype(request):
    if "application/json" in request.META['HTTP_ACCEPT']:
        return "application/json"
    else:
        return "text/plain"

#@csrf_exempt
def index(request):
    return render_to_response('index.html', RequestContext(request))

#@csrf_exempt
def new(request):
    return render_to_response('index_new.html', RequestContext(request))

#@csrf_exempt
def file_upload(request):
    """
    Check that a file upload can be updated into the POST dictionary without
    going pear-shaped.
    """

    if request.method == 'POST':
        upfile = request.FILES['upfile']

        user_tag = ''
        if request.user.username: 
            user_tag += request.user.username + '/'

        try:
            destfile = settings.MEDIA_UPLOAD_FILES_ROOT + user_tag + upfile.name
            dest = open(destfile, 'wb+')
            for chunk in upfile.chunks():
                dest.write(chunk)
            dest.close()
        except:
            return HttpResponse('fail to upload')

        dataUrl = settings.MEDIA_UPLOAD_FILE_URL + user_tag
        data = [{'url': dataUrl + upfile.name, 'name': upfile.name}]
        response = JSONResponse(data, {}, response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response
    else:
        return HttpResponse('Please use POST')

    data = [{'name': upfile.name}]
    response = JSONResponse(data, {}, response_mimetype(request))
    response['Content-Disposition'] = 'inline; filename=files.json'
    return response
#    return HttpResponseRedirect(reverse('index'))


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
            dest_dir = settings.MEDIA_UPLOAD_FILES_ROOT
            user_tag = ''
            if user:
                user_tag += user + '/'
            if tag_list_name:
                user_tag += tag_list_name + '/'
            dest_dir += user_tag
            try: 
                 tags = os.listdir(dest_dir)
            except:
                return HttpResponse('fail to list')
        
            dataUrl = settings.MEDIA_UPLOAD_FILE_URL + user_tag
            datas = []
            for tag in tags:
                data = [{'url': dataUrl + tag, 'name': tag}]
                datas = datas + data
            print simplejson.dumps(datas)
            return JSONResponse(datas)
#            return HttpResponse(simplejson.dumps(datas))
        else:
            return HttpResponse('Please specify tag list name')
    else:
        return HttpResponse('Please use GET')

    contents = []
    for tag in tags:
        contents = contents + ['<img src=' + settings.MEDIA_UPLOAD_FILE_URL + tag + '>']
    return HttpResponse(simplejson.dumps(contents));
#    return HttpResponse(simplejson.dumps(tags))
#    return render_to_response('index.html', {'tag_list': tags}, RequestContext(request))


def file_read(request):
    """
    Read one file content
    """

    fcontent = ''

    print 'reading file'
    if request.method == 'GET':
        user = request.user.username
        if request.GET.has_key('file_name'):
            file_name = request.GET['file_name']
            dest_file = settings.MEDIA_UPLOAD_FILES_ROOT
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

    return HttpResponse(fcontent)
#    return render_to_response('index.html', {'file_content': fcontent}, RequestContext(request))


def file_thumb(request):
    """
    Give a thumb of one file content
    """

    return HttpResponse()


class JSONResponse(HttpResponse):
    """JSON response class."""
    def __init__(self,obj='',json_opts={},mimetype="application/json",*args,**kwargs):
        content = simplejson.dumps(obj,**json_opts)
        print 'content in JSON resp'
        print content
        print mimetype
        super(JSONResponse,self).__init__(content,mimetype,*args,**kwargs)

