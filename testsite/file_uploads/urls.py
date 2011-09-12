from django.conf.urls.defaults import *
import views

urlpatterns = patterns('file_uploads.views',
    (r'^$',                 'index'),
    (r'^upload/$',          'file_upload'),
    (r'^list/$',            'file_list'),
    (r'^file/$',            'file_read'),
    (r'^thumb/$',           'file_thumb'),
    (r'^contact/$',         'contact'),
    (r'^thanks/$',          'thanks'),
#    (r'^.*',                'index'),
#    (r'^verify/$',          'file_upload_view_verify'),
#    (r'^unicode_name/$',    'file_upload_unicode_name'),
#    (r'^echo/$',            'file_upload_echo'),
#    (r'^quota/$',           'file_upload_quota'),
#    (r'^quota/broken/$',    'file_upload_quota_broken'),
#    (r'^getlist_count/$',   'file_upload_getlist_count'),
#    (r'^upload_errors/$',   'file_upload_errors'),
)
