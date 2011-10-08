from logging.handlers import SysLogHandler
import os

from django.conf import global_settings

ADMIN_MEDIA_PREFIX = '/media/admin/'
#CACHE_BACKEND = 'memcached://127.0.0.1:11211'
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': '/var/tmp/django_cache'
    }
}
DEBUG = True
DIRNAME = os.path.dirname(__file__)
#DATABASE_ENGINE = 'sqlite3'
#DATABASE_NAME = '/home/luoj/projects/web/uploaddemo/db/uploaddemo.db'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '/home/luoj/projects/web/uploaddemo/db/uploaddemo.db', # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.  
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}


# FILE_UPLOAD_HANDLERS is only necessary if you want to track upload
# progress in your Django app -- if you have a front-end proxy like
# nginx or lighttpd, Django doesn't need to be involved in the upload
# tracking.
FILE_UPLOAD_HANDLERS = ('uploaddemo.upload_handlers.UploadProgressCachedHandler', ) + global_settings.FILE_UPLOAD_HANDLERS
FILE_UPLOAD_MAX_MEMORY_SIZE = 1024768

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
MEDIA_ROOT = os.path.abspath(os.path.join(DIRNAME, 'media'))
MEDIA_URL = '/media/'
INSTALLED_APPS = (
    'uploaddemo',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)
ROOT_URLCONF = 'uploaddemo.urls'
SECRET_KEY = 'ew#y6%#96b%zp!98$dms5bp$f$gbg^)5_)ms)y@m6x_cf@g9oi'
TEMPLATE_DEBUG = DEBUG
TEMPLATE_LOADERS = (
#    'django.template.loaders.filesystem.load_template_source',
#    'django.template.loaders.app_directories.load_template_source',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
