#!/usr/bin/python
# -*- coding: UTF-8 -*-

from datetime import datetime
from django.contrib.markup.templatetags.markup import markdown
from django.db import models


class UltimoAggiornamento(models.Model):
    data = models.DateTimeField()

    class Meta:
        verbose_name_plural = u'Ultimo Aggiornamento'





class Parlamentare(models.Model):
    ADESIONE_SELECT = (
        ('0', 'Non risponde'),
        ('1', 'Aderisce'),
        ('2', 'Non aderisce'),
    )

    RAMO_PARLAMENTO_SELECT = (
        ('0', 'Camera'),
        ('1', 'Senato'),
    )


    def __unicode__(self):
        str = self.cognome+" "+self.nome

        if self.ramo_parlamento:
            str+=" - "+self.RAMO_PARLAMENTO_SELECT[int(self.ramo_parlamento)][1]
        if self.gruppo_parlamentare:
            str+=" - "+self.gruppo_parlamentare.sigla
        if self.adesione:
            str+=" - "+self.ADESIONE_SELECT[int(self.adesione)][1]
        return str

    class Meta:
        verbose_name_plural = u'Parlamentari'

    nome = models.CharField(max_length=50)
    cognome = models.CharField(max_length=50)
    ramo_parlamento = models.CharField(max_length=3,choices=RAMO_PARLAMENTO_SELECT, blank=True, default=None, null=True)
    gruppo_parlamentare = models.ForeignKey('GruppoParlamentare', null=True, blank=True, on_delete=models.SET_NULL)
    adesione = models.CharField(max_length=3,choices=ADESIONE_SELECT, blank=True, default=None, null=True)
    data_adesione = models.DateField(blank=True, null=True)
    gruppo_ristretto = models.BooleanField(default=False)
    in_carica = models.BooleanField(default=True)
    account_twitter = models.CharField(max_length=20, blank=True)
    risposta_twitter = models.BooleanField(default=False)
    account_mail = models.EmailField(max_length=100, blank=True)
    lettura_mail = models.BooleanField(default=False)
    risposta_mail = models.BooleanField(default=False)

    @classmethod
    def get_parlamentari_incarica(cls, ramo=None):

        group = Parlamentare.objects.filter(in_carica = True)
        if ramo is not None:
            group=group.filter(ramo_parlamento=ramo)

        return group

    @classmethod
    def get_senatori_incarica(cls):
        return Parlamentare.get_parlamentari_incarica('1')
    @classmethod
    def get_deputati_incarica(cls):
        return Parlamentare.get_parlamentari_incarica('0')

    @classmethod
    def get_n_parlamentari_incarica(cls, ramo=None):
        return Parlamentare.get_parlamentari_incarica(ramo).count()

    @classmethod
    def get_n_senatori_incarica(cls):
        return Parlamentare.get_n_parlamentari_incarica('1')
    @classmethod
    def get_n_deputati_incarica(cls):
        return Parlamentare.get_n_parlamentari_incarica('0')

    # returns all parlamentari / deputati / senatori in a state
    @classmethod
    def get_status(self, status, ramo=None):
        return self.get_parlamentari_incarica(ramo).filter(adesione=status)


    @classmethod
    def get_parlamentari_aderenti(cls):
        return Parlamentare.get_status('1')
    @classmethod
    def get_parlamentari_non_aderenti(cls):
        return Parlamentare.get_status('2')
    @classmethod
    def get_parlamentari_silenti(cls):
        return Parlamentare.get_status('0')

    @classmethod
    def get_n_parlamentari_aderenti(cls):
        return Parlamentare.get_parlamentari_aderenti().count()

    @classmethod
    def get_n_parlamentari_non_aderenti(cls):
        return Parlamentare.get_parlamentari_non_aderenti().count()

    @classmethod
    def get_n_parlamentari_silenti(cls):
        return Parlamentare.get_parlamentari_silenti().count()



    @classmethod
    def get_deputati_aderenti(cls):
        return Parlamentare.get_status('1','0')

    @classmethod
    def get_senatori_aderenti(cls):
        return Parlamentare.get_status('1','1')


    @classmethod
    def get_deputati_non_aderenti(cls):
        return Parlamentare.get_status('2','0')

    @classmethod
    def get_senatori_non_aderenti(cls):
        return Parlamentare.get_status('2','1')


    @classmethod
    def get_deputati_silenti(cls):
        return Parlamentare.get_status('0','0')

    @classmethod
    def get_senatori_silenti(cls):
        return Parlamentare.get_status('0','1')


    #n
    @classmethod
    def get_n_deputati_aderenti(cls):
        return Parlamentare.get_deputati_aderenti().count()

    @classmethod
    def get_n_senatori_aderenti(cls):
        return Parlamentare.get_senatori_aderenti().count()


    @classmethod
    def get_n_deputati_non_aderenti(cls):
        return Parlamentare.get_deputati_non_aderenti().count()

    @classmethod
    def get_n_senatori_non_aderenti(cls):
        return Parlamentare.get_senatori_non_aderenti().count()

    @classmethod
    def get_n_deputati_silenti(cls):
        return Parlamentare.get_deputati_non_aderenti().count()

    @classmethod
    def get_n_senatori_silenti(cls):
        return Parlamentare.get_senatori_non_aderenti().count()



class GruppoParlamentare(models.Model):
    class Meta:
        verbose_name_plural = u'Gruppi Parlamentari'

    def __unicode__(self):
        return self.nome

    nome = models.CharField(max_length=50)
    sigla = models.CharField(max_length=10)
    data_creazione = models.DateField(blank=True, null=True)


    @classmethod
    def get_gruppi(cls):
        return GruppoParlamentare.objects.all()

    def get_parlamentari(self, ramo=None):
        return Parlamentare.get_parlamentari_incarica(ramo).filter(gruppo_parlamentare=self)

    # returns all parlamentari / deputati / senatori in a state
    def get_status(self, status, ramo=None):
        return self.get_parlamentari(ramo).filter(adesione=status)

    def get_aderenti(self, ramo=None):
        return self.get_status('1',ramo)

    def get_non_aderenti(self, ramo=None):
        return self.get_status('2',ramo)

    def get_silenti(self, ramo=None):
        return self.get_status('0',ramo)

    def get_perc_aderenti(self, ramo=None):
        return self.get_aderenti(ramo)/self.get_parlamentari(ramo)

    def get_perc_non_aderenti(self, ramo=None):
        return self.get_non_aderenti(ramo)/self.get_parlamentari(ramo)

    def get_perc_silenti(self, ramo=None):
        return self.get_silenti(ramo)/self.get_parlamentari(ramo)



class Entry(models.Model):
    COLONNA_SELECT = (
        ('0', 'Sinistra'),
        ('1', 'Destra'),
    )
    title= models.CharField(max_length=255)
    author=models.CharField(max_length=255, null=True, blank=True)
    body= models.TextField()
    body_html = models.TextField(editable=False, default="")
    published_at= models.DateTimeField(default=datetime.now())
    published=models.BooleanField(default=False)
    colonna=models.CharField(max_length=3,choices=COLONNA_SELECT, default=False)

    def __unicode__(self):
        return u"%s - %s" %(self.published_at.date(), self.title)


    class Meta():
        verbose_name= 'articolo'
        verbose_name_plural= 'News'

    def save(self):
        super(Entry, self).save()
        if self.body:
            self.body_html= markdown(self.body)

        super(Entry, self).save()



