from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('pi.views',
    # Examples:
    # url(r'^$', 'pi.views.home', name='home'),
    # url(r'^pi/', include('pi.foo.urls')),
    url(r'^$',                 'index', name='index'),
    url(r'^upload/$',          'file_upload', name='file_upload'),
    url(r'^upload_progress/$', 'upload_progress', name='upload_progress'),
    url(r'^list/$',            'file_list', name='file_list'),
    url(r'^file/$',            'file_read', name='file_read'),
    url(r'^thumb/$',           'file_thumb', name='file_thumb'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
