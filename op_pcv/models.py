#!/usr/bin/python
# -*- coding: UTF-8 -*-


from django.db import models
from django.conf import settings


class Parlamentare(models.Model):
    def __unicode__(self):
        return self.nome

    class Meta:
        verbose_name_plural = u'Parlamentari'

    ADESIONE_SELECT = (

        (1, 'Aderisce'),
        (2, 'Non risponde'),
        (3, 'Non aderisce'),
    )

    RAMO_PARLAMENTO_SELECT=(

        (1, 'Parlamento'),
        (2, 'Senato'),
    )

    GRUPPO_SELECT=(

        (1,'Popolo della Libertà'),
        (2,'Partito Democratico'),
        (3,'Movimento 5 stelle'),
        (4,'Scelta civica per l\'Italia'),
        (5,'Sinistra ecologia e libertà'),
        (6, 'Lega Nord e autonomie'),
        (7,'Fratelli d\'Italia - Centrodestra Nazionale'),
        (8, 'Gruppo per le autonomie-Psi'),
        (9,'Gruppo Misto'),
        (10,'Grandi autonomie e libertà'),
    )

    nome = models.CharField(max_length=50)
    cognome = models.CharField(max_length=50)
    account_twitter = models.CharField(max_length=20, blank=True)
    gruppo_parlamentare = models.IntegerField(choices=GRUPPO_SELECT, blank=True, default=None)
    risposta_twitter = models.BooleanField(default=False)
    account_mail = models.EmailField(max_length=100, blank=True)

    lettura_mail = models.BooleanField(default=False)
    risposta_mail = models.BooleanField(default=False)
    adesione = models.IntegerField(choices=ADESIONE_SELECT, blank=True, default=None)
    ramo_parlamento = models.IntegerField(choices=RAMO_PARLAMENTO_SELECT, blank=True, default=None)
    attivo = models.BooleanField(default=True)
    gruppo_ristretto = models.BooleanField(default=False)
    data_adesione = models.DateField(blank=True, null=True)