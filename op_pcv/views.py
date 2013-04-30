from django.conf import settings
from django.shortcuts import render_to_response
from django.views.generic import TemplateView
from op_pcv.models import Parlamentare,GruppoParlamentare, UltimoAggiornamento, Entry
import feedparser
from django.core.cache import cache
from settings import OP_BLOG_FEED

class PcvHome(TemplateView):
    template_name = "home.html"
    context={}

    def get_context_data(self, **kwargs):
        context = super(PcvHome,self).get_context_data(**kwargs)

        context['pie_senato']={}
        context['pie_senato']['non_aderenti']=Parlamentare.get_n_senatori_silenti()+Parlamentare.get_n_senatori_non_aderenti()
        context['pie_senato']['aderenti']=Parlamentare.get_n_senatori_aderenti()
        context['pie_senato']['totale']=Parlamentare.get_n_senatori_incarica()
        context['pie_camera']={}
        context['pie_camera']['non_aderenti']=Parlamentare.get_n_deputati_silenti()+Parlamentare.get_n_deputati_non_aderenti()
        context['pie_camera']['aderenti']=Parlamentare.get_n_deputati_aderenti()
        context['pie_camera']['totale']=Parlamentare.get_n_deputati_incarica()

        gruppi=GruppoParlamentare.get_gruppi()
        context['dati_gruppi']=[]
        for g in gruppi:

            mydict={}
            mydict["sigla"]=g.sigla
            mydict["aderenti_tot"]=g.get_n_aderenti()
            mydict["non_aderenti_tot"]=g.get_n_non_aderenti()+g.get_n_silenti()
            context['dati_gruppi'].append(mydict)


        # feeds are extracted and cached for one hour (memcached)
        feeds = cache.get('op_associazione_home_feeds')
        if feeds is None:
            feeds = {}
            feeds['blog'] = feedparser.parse(OP_BLOG_FEED)
            cache.set('op_associazione_home_feeds', feeds, 3600)


        return context
