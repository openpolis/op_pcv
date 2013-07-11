from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from op_pcv.views import PcvHome,PcvLista

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin', include(admin.site.urls)),
    url(r'^$', PcvHome.as_view(), name="home"),
    url(r'^lista/(?P<tipologia>[-\w]*)(?:/(?P<adesione>[-\w]*))?$', PcvLista.as_view(), name="lista"),
    # url(r'^op_pcv/', include('op_pcv.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # work in progress url
    #url(r'^.*$', TemplateView.as_view(template_name='lavorincorso.html')),



)
