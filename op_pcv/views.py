import socket
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response
from django.views.generic import TemplateView
from op_pcv.models import Parlamentare,GruppoParlamentare, UltimoAggiornamento, Entry
import feedparser
from utils import remove_img_tags
<<<<<<< HEAD
from django.core.cache import cache
=======
>>>>>>> b053c1d8f19fb6241370db23e53cfbd45d3330a5
import time
import logging



class PcvLista(TemplateView):

    template_name = "lista.html"

    def get_context_data(self, **kwargs):
        context = super(PcvLista, self).get_context_data(**kwargs)

        tipo = kwargs['tipologia']
        adesione = kwargs['adesione']

        if tipo == "deputati" or tipo=="senatori" or tipo=="":
            context['tipologia'] = tipo
        else:
            context['tipologia'] = ""

        if adesione == "aderiscono" or adesione =="non_aderiscono":
            context['ordinamento'] = adesione
        else:
            context['ordinamento']=''


        context['n_deputati']=Parlamentare.get_n_deputati_incarica()
        context['n_senatori']=Parlamentare.get_n_senatori_incarica()
        context['n_totale']=Parlamentare.get_n_parlamentari_incarica()

        dep = Parlamentare.get_deputati_incarica()
        sen = Parlamentare.get_senatori_incarica()
        par = Parlamentare.get_parlamentari_incarica()
        # rende maiuscola la prima lettera di ogni parola del cognome
        if dep is not None:
            for p in dep:
                p.cognome=p.cognome.title()

        # rende maiuscola la prima lettera di ogni parola del cognome
        if sen is not None:
            for p in sen:
                p.cognome=p.cognome.title()

        # rende maiuscola la prima lettera di ogni parola del cognome
        if par is not None:
            for p in par:
                p.cognome=p.cognome.title()


        context['lista_deputati']=dep
        context['lista_senatori']=sen
        context['lista_completa']=par

        return context



class PcvHome(TemplateView):
    template_name = "home.html"
    context={}
    logger = logging.getLogger('feed')    

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
        ordine_gruppi_camera=["Pd","Pdl","M5S","Sc","Sel","Lega","Misto","Fdi"]
        ordine_gruppi_senato=["Pd","Pdl","M5S","Sc","Lega","Gal","Aut-Psi","Misto"]

        for sigla in ordine_gruppi_camera:
            try:
                g = GruppoParlamentare.objects.get(sigla=sigla)
            except ObjectDoesNotExist:
                break
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

        context['gruppi_didascalia']=GruppoParlamentare.get_gruppi()

        blogposts = []
        # sets the timeout for the socket connection
        socket.setdefaulttimeout(100)
        feeds = feedparser.parse(settings.OP_BLOG_FEED)
        context['feeds_entries'] = len(feeds.entries)


        if feeds is not None:
            i=0
            post_counter = 0

            while i<len(feeds.entries) and post_counter < 3 :
                if 'tags' in feeds.entries[i]:
                    for tag in feeds.entries[i].tags:
                        if tag.term == settings.OP_BLOG_PCV_TAG:
                            feeds.entries[i]['content'][0]['value']=remove_img_tags(feeds.entries[i]['content'][0]['value'])
                            feeds.entries[i]['published'] = time.strftime("%d.%m.%Y",time.strptime(feeds.entries[i]['published'], '%a, %d %b %Y %H:%M:%S +0000'))
                            blogposts.append(feeds.entries[i])
                            post_counter += 1

                i += 1


        context['blogposts']=blogposts

        # adesioni count and adesioni lists

        context['n_dep_aderiscono']=Parlamentare.get_n_deputati_aderenti()
        context['n_dep_nonaderiscono']=Parlamentare.get_n_deputati_neg_aderenti()

        context['n_sen_aderiscono']=Parlamentare.get_n_senatori_aderenti()
        context['n_sen_nonaderiscono']=Parlamentare.get_n_senatori_neg_aderenti()

        dep_aderenti = Parlamentare.get_deputati_aderenti(True)[:10]
        sen_aderenti = Parlamentare.get_senatori_aderenti(True)[:10]

        dep_naderenti = Parlamentare.get_deputati_neg_aderenti(True)[:10]
        sen_naderenti = Parlamentare.get_senatori_neg_aderenti(True)[:10]

        # rende maiuscola la prima lettera di ogni parola del cognome
        if dep_aderenti is not None:
            for p in dep_aderenti:
                p.cognome=p.cognome.title()

        # rende maiuscola la prima lettera di ogni parola del cognome
        if sen_aderenti is not None:
            for p in sen_aderenti:
                p.cognome=p.cognome.title()

        # rende maiuscola la prima lettera di ogni parola del cognome
        if dep_naderenti is not None:
            for p in dep_naderenti:
                p.cognome=p.cognome.title()

        # rende maiuscola la prima lettera di ogni parola del cognome
        if sen_naderenti is not None:
            for p in sen_naderenti:
                p.cognome=p.cognome.title()

        context['dep_aderiscono'] = dep_aderenti
        context['sen_aderiscono'] = sen_aderenti

        context['dep_neg_aderiscono'] = dep_naderenti
        context['sen_neg_aderiscono'] = sen_naderenti


        return context
