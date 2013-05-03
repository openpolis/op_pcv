from django.conf import settings
from django.shortcuts import render_to_response
from django.views.generic import TemplateView
from op_pcv.models import Parlamentare,GruppoParlamentare, UltimoAggiornamento, Entry
import feedparser
from django.core.cache import cache
from settings import OP_BLOG_FEED,OP_BLOG_PCV_TAG,OP_BLOG_CACHETIME

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
        blogpost = cache.get('op_associazione_home_feeds')

        if blogpost is None:

            feeds = feedparser.parse(OP_BLOG_FEED)
            i=0
            trovato=False
            while i<len(feeds.entries) and not trovato:
                for tag in feeds.entries[i].tags:
                    if tag.term == OP_BLOG_PCV_TAG:
                        trovato=True

                if not trovato:
                    i += 1

            blogpost = feeds.entries[i]
            cache.set('op_associazione_home_feeds', blogpost , OP_BLOG_CACHETIME)

        context['blogpost']=blogpost

        # adesioni count and adesioni lists

        context['n_dep_aderiscono']=Parlamentare.get_n_deputati_aderenti()
        context['n_dep_nonaderiscono']=Parlamentare.get_n_deputati_neg_aderenti()

        context['n_sen_aderiscono']=Parlamentare.get_n_senatori_aderenti()
        context['n_sen_nonaderiscono']=Parlamentare.get_n_senatori_neg_aderenti()

        context['dep_aderiscono'] = Parlamentare.get_deputati_aderenti()[:10]
        context['sen_aderiscono'] = Parlamentare.get_senatori_aderenti()[:10]

        context['dep_neg_aderiscono'] = Parlamentare.get_deputati_neg_aderenti()[:10]
        context['sen_neg_aderiscono'] = Parlamentare.get_senatori_neg_aderenti()[:10]

        return context
