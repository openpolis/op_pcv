from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from op_pcv.views import PcvHome

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin', include(admin.site.urls)),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # work in progress url
    #url(r'^.*$', TemplateView.as_view(template_name='lavorincorso.html')),

    url(r'^$', PcvHome.as_view(), name="home"),


)
