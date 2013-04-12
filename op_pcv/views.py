from django.conf import settings
from django.shortcuts import render_to_response
from django.views.generic import TemplateView


class PcvHome(TemplateView):
    template_name = "home.html"
    def get_context_data(self, **kwargs):



        return render_to_response('home.html')
