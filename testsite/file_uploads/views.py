import os
from django.core.files.uploadedfile import UploadedFile
from django.http import HttpResponse, HttpResponseServerError, HttpResponseRedirect
from django.utils import simplejson
from models import FileModel, ContactForm
from django.utils.hashcompat import sha_constructor
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt, csrf_protect

@csrf_exempt
def index(request):
    if request.method == 'GET':
        print request.path_info
        if request.path_info == "/file_uploads/":
            return render_to_response('file_uploads/index.html')
        else: 
            return HttpResponse(request.path_info)
    else:
#       request.method == 'POST':
        if request.POST.has_key('fileName'):
            fname = request.POST['fileName']
            data = request.POST['data']
        else:
            fname = "myname"
        print fname
        print data
        print request.user
        return render_to_response('file_uploads/index.html', {
                                    'fname': fname,
                                    'data':  data, 
                                  })

@csrf_exempt
def file_upload(request):
    """
    Check that a file upload can be updated into the POST dictionary without
    going pear-shaped.
    """
    response = HttpResponse()

    if request.method == 'POST':
        upfile = request.FILES['upfile']
        user = request.user.username
        try:
            destfile = "/tmp/django/" + user + "/" + upfile.name
#           destfile = "/tmp/roottmp/" + upfile.name
            dest = open(destfile, 'wb+')
            for chunk in upfile.chunks():
                dest.write(chunk)
            ret = dest.close()
            print ret
        except:
            response.write("fail to upload")
            return response
    else:
        response.write("use POST instead of GET")
        return response

    response.write("success")
    response['Tags'] = "tag1:tag2"
    return response


@csrf_exempt
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            print "===="
            print form.cleaned_data['message']
            return HttpResponseRedirect('/file_uploads/thanks/')
    else:
        form = ContactForm()

    print "contact.html"

    return render_to_response('file_uploads/contact.html', {'form': form,})


def thanks(request):
    response = HttpResponse('thanks')
    return response

def download(request):
    response = HttpResponse('download')
    response['Content-Disposition'] = 'attachment; filename=/tmp/django/date1.txt'
    return response


@csrf_exempt
def meta_upload(request):
    """
    Check that a meta upload can be updated into the POST dictionary without
    going pear-shaped.
    """

    return HttpResponse('success')


def old_file(request):
    form_data = request.POST.copy()
    form_data.update(request.FILES)
    if isinstance(form_data.get('file_field'), UploadedFile) and isinstance(form_data['name'], unicode):
        # If a file is posted, the dummy client should only post the file name,
        # not the full path.
        if os.path.dirname(form_data['file_field'].name) != '':
            return HttpResponseServerError()
        return HttpResponse('')
    else:
        return HttpResponseServerError()

def file_upload_view_verify(request):
    """
    Use the sha digest hash to verify the uploaded contents.
    """
    form_data = request.POST.copy()
    form_data.update(request.FILES)

    for key, value in form_data.items():
        if key.endswith('_hash'):
            continue
        if key + '_hash' not in form_data:
            continue
        submitted_hash = form_data[key + '_hash']
        if isinstance(value, UploadedFile):
            new_hash = sha_constructor(value.read()).hexdigest()
        else:
            new_hash = sha_constructor(value).hexdigest()
        if new_hash != submitted_hash:
            return HttpResponseServerError()

    # Adding large file to the database should succeed
    largefile = request.FILES['file_field2']
    obj = FileModel()
    obj.testfile.save(largefile.name, largefile)

    return HttpResponse('')

def file_upload_unicode_name(request):

    # Check to see if unicode name came through properly.
    if not request.FILES['file_unicode'].name.endswith(UNICODE_FILENAME):
        return HttpResponseServerError()

    response = None

    # Check to make sure the exotic characters are preserved even
    # through file save.
    uni_named_file = request.FILES['file_unicode']
    obj = FileModel.objects.create(testfile=uni_named_file)
#    full_name = u'%s/%s' % (UPLOAD_TO, uni_named_file.name)
    if not os.path.exists(full_name):
        response = HttpResponseServerError()

    # Cleanup the object with its exotic file name immediately.
    # (shutil.rmtree used elsewhere in the tests to clean up the
    # upload directory has been seen to choke on unicode
    # filenames on Windows.)
    obj.delete()
    os.unlink(full_name)

    if response:
        return response
    else:
        return HttpResponse('')

def file_upload_echo(request):
    """
    Simple view to echo back info about uploaded files for tests.
    """
    r = dict([(k, f.name) for k, f in request.FILES.items()])
    return HttpResponse(simplejson.dumps(r))

def file_upload_quota(request):
    """
    Dynamically add in an upload handler.
    """
    request.upload_handlers.insert(0, QuotaUploadHandler())
    return file_upload_echo(request)

def file_upload_quota_broken(request):
    """
    You can't change handlers after reading FILES; this view shouldn't work.
    """
    response = file_upload_echo(request)
    request.upload_handlers.insert(0, QuotaUploadHandler())
    return response

def file_upload_getlist_count(request):
    """
    Check the .getlist() function to ensure we receive the correct number of files.
    """
    file_counts = {}

    for key in request.FILES.keys():
        file_counts[key] = len(request.FILES.getlist(key))
    return HttpResponse(simplejson.dumps(file_counts))

def file_upload_errors(request):
    request.upload_handlers.insert(0, ErroringUploadHandler())
    return file_upload_echo(request)
