from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib import admin
from sq_admin.urls import admin_urls

admin.autodiscover()


urlpatterns = patterns('', url(r'^$', direct_to_template, {'template': 'index.html'}, 'index'))

urlpatterns += admin_urls

urlpatterns += patterns('',

    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    (r'^media/images/*$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
    {'document_root': settings.STATIC_ROOT}),
)
