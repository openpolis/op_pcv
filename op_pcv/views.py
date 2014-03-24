import copy
import datetime
import socket
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.views.generic import TemplateView
from op_pcv.models import Parlamentare,GruppoParlamentare, UltimoAggiornamento, Entry
import feedparser
from utils import remove_img_tags
import logging
import locale



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

        # sets order for groups in the col chart

        ordine_gruppi_camera = GruppoParlamentare.objects.\
            filter(parlamentare__ramo_parlamento='0',parlamentare__in_carica=True).\
            annotate(n=Count("parlamentare")).order_by('-n')
        ordine_gruppi_senato = GruppoParlamentare.objects. \
            filter(parlamentare__ramo_parlamento='1',parlamentare__in_carica=True). \
            annotate(n=Count("parlamentare")).order_by('-n')

        for gruppo_camera in ordine_gruppi_camera:
            gruppo_c={}
            gruppo_c["sigla"]=gruppo_camera.sigla
            gruppo_c["aderenti_tot"]=gruppo_camera.get_n_aderenti(0)
            gruppo_c["non_aderenti_tot"]=gruppo_camera.get_n_non_aderenti(0)+gruppo_camera.get_n_silenti(0)
            context['col_camera'].append(gruppo_c)


        context['col_senato']=[]

        for gruppo_senato in ordine_gruppi_senato:
            gruppo_s={}
            gruppo_s["sigla"]=gruppo_senato.sigla
            gruppo_s["aderenti_tot"]=gruppo_senato.get_n_aderenti(1)
            gruppo_s["non_aderenti_tot"]=gruppo_senato.get_n_non_aderenti(1)+gruppo_senato.get_n_silenti(1)
            context['col_senato'].append(gruppo_s)

        context['gruppi_didascalia']=GruppoParlamentare.get_gruppi()

        blogposts = []
        # sets the timeout for the socket connection
        socket.setdefaulttimeout(100)
        feedparser._HTMLSanitizer.acceptable_elements = feedparser._HTMLSanitizer.acceptable_elements.union(set(["object", "embed", "iframe"]))
        entries = feedparser.parse(settings.OP_BLOG_FEED).entries
        context['feeds_entries'] = len(entries)

        if entries is not None:
            for entry in entries:

                if len(blogposts) > 2:
                    break

                if 'tags' in entry:

                    category_found = False
                    for tag in entry.tags:
                        if tag.term == settings.OP_BLOG_PCV_CATEGORY:
                            category_found = True
                            break

                    if category_found:
                        entry_dict = {
                                      'link': entry['link'],
                                      'title': entry['title'].upper(),
                                      }

                        post_content = entry['content'][0]['value']
                        feedburner_string = '<p>The post <a'
                        entry_dict['content'] = post_content.split(feedburner_string)[0]

                        # set locale to en, to parse the post timestamp
                        locale.setlocale(locale.LC_ALL, 'en_US.utf8')
                        post_date = datetime.datetime.strptime(entry['published'], '%a, %d %b %Y %H:%M:%S +0000')

                        # set locale to it, to produced localized months' names
                        locale.setlocale(locale.LC_ALL, 'it_IT.utf8')

                        entry_dict['month'] = post_date.strftime('%b').upper()
                        entry_dict['day'] = post_date.strftime('%d')
                        entry_dict['year'] = post_date.strftime('%Y')

                        blogposts.append(entry_dict)



        locale.setlocale(locale.LC_ALL, 'en_US.utf8')
        
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
