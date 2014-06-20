from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'core.views.index', name='index'),
    url(r'^download/$', 'core.views.download_page', name='download'),
    url(r'^admin/', include(admin.site.urls)),
)
