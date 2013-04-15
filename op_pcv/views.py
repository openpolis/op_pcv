from django.conf import settings
from django.shortcuts import render_to_response
from django.views.generic import TemplateView
from op_pcv.models import Parlamentare,GruppoParlamentare, UltimoAggiornamento


class PcvHome(TemplateView):
    template_name = "home.html"
    context={}

    def get_context_data(self, **kwargs):
        context = super(PcvHome,self).get_context_data(**kwargs)

        context['adesione_codes']=[0,1,2]

        context['totale']={}
        context['totale'][0]={}
        context['totale'][1]={}
        context['totale'][1][0]=Parlamentare.get_n_senatori_silenti()
        context['totale'][1][1]=Parlamentare.get_n_senatori_aderenti()
        context['totale'][1][2]=Parlamentare.get_n_senatori_non_aderenti()

        context['totale'][0][0]=Parlamentare.get_n_deputati_silenti()
        context['totale'][0][1]=Parlamentare.get_n_deputati_aderenti()
        context['totale'][0][2]=Parlamentare.get_n_deputati_non_aderenti()

        gruppi=GruppoParlamentare.get_gruppi()
        context['dati_gruppi']=[]
        for g in gruppi:

            mydict={}
            mydict["sigla"]=g.sigla
            mydict["aderenti_tot"]=g.get_aderenti()
            mydict["non_aderenti_tot"]=g.get_non_aderenti()
            mydict["silenti_tot"]=g.get_silenti()
            context['dati_gruppi'].append(mydict)


        return context
