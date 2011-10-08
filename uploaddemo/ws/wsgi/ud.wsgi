import os, sys

#sys.path.append("/usr/local/django/test")
sys.path.append("/home/luoj/projects/web")

os.environ['DJANGO_SETTINGS_MODULE'] = 'uploaddemo.settings'
import django.core.handlers.wsgi

_application = django.core.handlers.wsgi.WSGIHandler()

def application(environ, start_response):
    environ['PATH_INFO'] = environ['SCRIPT_NAME'] + environ['PATH_INFO']
    return _application(environ, start_response)
