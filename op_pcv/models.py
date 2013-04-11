#!/usr/bin/python
# -*- coding: UTF-8 -*-


from django.db import models


class UltimoAggiornamento(models.Model):
    data = models.DateTimeField()

    class Meta:
        verbose_name_plural = u'Ultimo Aggiornamento'


class GruppoParlamentare(models.Model):
    class Meta:
        verbose_name_plural = u'Gruppi Parlamentari'

    def __unicode__(self):
        return self.nome

    nome = models.CharField(max_length=50)
    sigla = models.CharField(max_length=10)
    data_creazione = models.DateField(blank=True, null=True)


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
