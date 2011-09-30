import os, sys

sys.path.append("/home/luoj/projects/git/test1")

os.environ['DJANGO_SETTINGS_MODULE'] = 'pi.settings'
import django.core.handlers.wsgi

_application = django.core.handlers.wsgi.WSGIHandler()

def application(environ, start_response):
    environ['PATH_INFO'] = environ['SCRIPT_NAME'] + environ['PATH_INFO']
    return _application(environ, start_response)
