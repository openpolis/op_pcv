#!/usr/bin/python
# -*- coding: UTF-8 -*-


from django.db import models


class UltimoAggiornamento(models.Model):
    ultimo_aggiornamento = models.DateTimeField()

    class Meta:
        verbose_name_plural = u'Ultimo Aggiornamento'


class Parlamentare(models.Model):
    ADESIONE_SELECT = (
        ('0', 'Aderisce'),
        ('1', 'Non risponde'),
        ('2', 'Non aderisce'),
    )

    RAMO_PARLAMENTO_SELECT = (
        ('0', 'Camera'),
        ('1', 'Senato'),
    )

    GRUPPO_SELECT = (
        ('0','Popolo della Libertà'),
        ('1','Partito Democratico'),
        ('2','Movimento 5 stelle'),
        ('3','Scelta civica per l\'Italia'),
        ('4','Sinistra ecologia e libertà'),
        ('5','Lega Nord e autonomie'),
        ('6','Fratelli d\'Italia - Centrodestra Nazionale'),
        ('7','Gruppo per le autonomie-Psi'),
        ('8','Gruppo Misto'),
        ('9','Grandi autonomie e libertà'),
    )

    def __unicode__(self):
        str = self.nome+" "+self.cognome

        if self.ramo_parlamento:
            str+=" - "+self.RAMO_PARLAMENTO_SELECT[int(self.ramo_parlamento)][1]
        if self.gruppo_parlamentare:
            str+=" - "+self.GRUPPO_SELECT[int(self.gruppo_parlamentare)][1]
        if self.adesione:
            str+=" - "+self.ADESIONE_SELECT[int(self.adesione)][1]
        return str

    class Meta:
        verbose_name_plural = u'Parlamentari'

    nome = models.CharField(max_length=50)
    cognome = models.CharField(max_length=50)
    account_twitter = models.CharField(max_length=20, blank=True)
    gruppo_parlamentare = models.CharField(max_length=3,choices=GRUPPO_SELECT, blank=True, default=None)
    risposta_twitter = models.BooleanField(default=False)
    account_mail = models.EmailField(max_length=100, blank=True)
    lettura_mail = models.BooleanField(default=False)
    risposta_mail = models.BooleanField(default=False)
    adesione = models.CharField(max_length=3,choices=ADESIONE_SELECT, blank=True, default=None)
    ramo_parlamento = models.CharField(max_length=3,choices=RAMO_PARLAMENTO_SELECT, blank=True, default=None)
    attivo = models.BooleanField(default=True)
    gruppo_ristretto = models.BooleanField(default=False)
    data_adesione = models.DateField(blank=True, null=True)