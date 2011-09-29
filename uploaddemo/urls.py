from django.conf import settings
from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('uploaddemo.views',
    url(r'^$', 'list', name='uploads'),
    url(r'^confirm/delete/$', 'confirm_delete', name='confirm_delete'),
    url(r'^delete/$', 'delete', name='delete'),
    url(r'^upload/$', 'upload', name='upload'),
    url(r'^upload/progress/$', 'upload_progress', name='upload_progress'),
)

urlpatterns += patterns('',
    (r'^account/login/$', 'django.contrib.auth.views.login'),
    (r'^account/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
#    (r'^admin/(.*)', admin.site.root),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
