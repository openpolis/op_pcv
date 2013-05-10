import socket
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response
from django.views.generic import TemplateView, ListView
from op_pcv.models import Parlamentare,GruppoParlamentare, UltimoAggiornamento, Entry
import feedparser
from django.core.cache import cache
from settings import OP_BLOG_FEED,OP_BLOG_PCV_TAG,OP_BLOG_CACHETIME



class PcvLista(ListView):
    model=Parlamentare
    template_name = "lista.html"

    def get_context_data(self, **kwargs):
        context = super(PcvLista, self).get_context_data(**kwargs)
        context['n_deputati']=Parlamentare.get_n_deputati_incarica()
        context['n_senatori']=Parlamentare.get_n_senatori_incarica()
        context['n_totale']=Parlamentare.get_n_parlamentari_incarica()

        return context

    def get_queryset(self):
        return  Parlamentare.objects.all()

class PcvHome(TemplateView):
    template_name = "home.html"
    context={}

    def get_context_data(self, **kwargs):
        context = super(PcvHome,self).get_context_data(**kwargs)

        # data for pie charts
        context['pie_senato']={}
        context['pie_senato']['non_aderenti']=Parlamentare.get_n_senatori_silenti()+Parlamentare.get_n_senatori_non_aderenti()
        context['pie_senato']['aderenti']=Parlamentare.get_n_senatori_aderenti()
        context['pie_senato']['totale']=Parlamentare.get_n_senatori_incarica()
        context['pie_camera']={}
        context['pie_camera']['non_aderenti']=Parlamentare.get_n_deputati_silenti()+Parlamentare.get_n_deputati_non_aderenti()
        context['pie_camera']['aderenti']=Parlamentare.get_n_deputati_aderenti()
        context['pie_camera']['totale']=Parlamentare.get_n_deputati_incarica()

        # data for adesioni coloumn charts

        context['col_camera']=[]

        # sets fixed order for groups in the col chart
        ordine_gruppi_camera=["PD","PDL","M5S","SC","SEL","LEGA","MISTO","FDI"]
        ordine_gruppi_senato=["PD","PDL","M5S","SC","LEGA","GAL","GPA-PSI","MISTO"]

        for sigla in ordine_gruppi_camera:
            try:
                g = GruppoParlamentare.objects.get(sigla=sigla)
            except ObjectDoesNotExist:
                pass
            mydict={}
            mydict["sigla"]=g.sigla
            mydict["aderenti_tot"]=g.get_n_aderenti(0)
            mydict["non_aderenti_tot"]=g.get_n_non_aderenti(0)+g.get_n_silenti(0)
            context['col_camera'].append(mydict)


        context['col_senato']=[]

        for sigla in ordine_gruppi_senato:
            try:
                g = GruppoParlamentare.objects.get(sigla=sigla)
            except ObjectDoesNotExist:
                pass

            mydict={}
            mydict["sigla"]=g.sigla
            mydict["aderenti_tot"]=g.get_n_aderenti(1)
            mydict["non_aderenti_tot"]=g.get_n_non_aderenti(1)+g.get_n_silenti(1)
            context['col_senato'].append(mydict)

        # feeds are extracted and cached for one hour (memcached)
        blogpost = cache.get('op_associazione_home_feeds')


        blogpost=None
        if blogpost is None:
            # sets the timeout for the socket connection
            socket.setdefaulttimeout(150)
            feeds = feedparser.parse(OP_BLOG_FEED)
            if feeds is not None:
                i=0
                trovato=False
                while i<len(feeds.entries) and not trovato:
                    if 'tags' in feeds.entries[i]:
                        for tag in feeds.entries[i].tags:
                            if tag.term == OP_BLOG_PCV_TAG:
                                trovato=True

                    if not trovato:
                        i += 1

                if trovato is True:
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
