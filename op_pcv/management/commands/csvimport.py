# -*- coding: utf-8 -*-

# metadata Deputato,Gruppo,Account twitter,Risposta twitter,Contatto mail,Lettura mail,Risposta mail,Adesione

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import connection
from django.db.utils import DatabaseError
from django.core.management.base import BaseCommand, CommandError
from decimal import Decimal
from django.template.defaultfilters import slugify
from op_pcv import utils
from op_pcv.models import *
from optparse import make_option
import csv
import logging
from datetime import datetime
from django.utils import timezone
from HTMLParser import HTMLParser


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ' '.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


class Command(BaseCommand):

    help = 'Import data from CSV'

    option_list = BaseCommand.option_list + (
        make_option('--csv-file',
                    dest='csvfile',
                    default='./file.csv',
                    help='Select csv file'),
        make_option('--type',
                    dest='type',
                    default=None,
                    help='Type of import: dep|sen'),
        make_option('--update',
                    dest='update',
                    action='store_true',
                    default=False,
                    help='Update Existing Records: True|False'),
        make_option('--delete',
                    dest='delete',
                    action='store_true',
                    default=False,
                    help='Delete Existing Records: True|False'),
    )

    csv_file = ''
    encoding = 'utf8'
    #    encoding='latin1'
    logger = logging.getLogger('csvimport')
    unicode_reader = None

    def handle(self, *args, **options):

        self.csv_file = options['csvfile']
        self.logger.info('CSV FILE "%s"\n' % self.csv_file )

        # read first csv file
        try:
            self.unicode_reader = \
                utils.UnicodeDictReader(open(self.csv_file, 'r'), encoding=self.encoding, dialect="excel")
        except IOError:
            self.logger.error("It was impossible to open file %s\n" % self.csv_file)
            exit(1)
        except csv.Error, e:
            self.logger.error("CSV error while reading %s: %s\n" % (self.csv_file, e.message))


        if options['type'] == 'dep':
            self.handle_dep(*args, **options)
            UltimoAggiornamento.objects.all().update(data_progetti=timezone.now())
        elif options['type'] == 'sen':
            self.handle_sen(*args, **options)
            UltimoAggiornamento.objects.all().update(data_progetti=timezone.now())
        else:
            self.logger.error("Wrong type %s. Select among dep, sen." % options['type'])
            exit(1)

    def handle_dep(self, *args, **options):
        c = 0

        if options['delete']:
            self.logger.info("Erasing the precedently stored data...")
            Parlamentare.objects.filter(ramo_parlamento=1).delete()

        self.logger.info("Inizio import da %s" % self.csv_file)

        # for r in self.unicode_reader:
        #
        #
        #     updated = False
        #
        #     territorio = Territorio.objects.get(cod_comune=r['istat'])
        #
        #     try:
        #         tipologia = TipologiaProgetto.objects.get(codice=r['tipologia'])
        #     except ObjectDoesNotExist:
        #         tipologia = TipologiaProgetto.objects.get(denominazione="Altro")
        #
        #     self.logger.info("%s: Analizzando record: %s" % ( r['istat'],r['id_progetto']))
        #     importo_previsto=r['importo_previsto'].replace('$','')
        #     riepilogo_importi=r['riepilogo_importi'].replace(',','.')
        #
        #     progetto, created = Progetto.objects.get_or_create(
        #         id_progetto = r['id_progetto'],
        #         id_padre__isnull = True,
        #
        #         defaults={
        #             'id_progetto': r['id_progetto'],
        #             'territorio': territorio,
        #             'denominazione': strip_tags(r['denominazione']),
        #             'importo_previsto': importo_previsto,
        #             'riepilogo_importi': Decimal(riepilogo_importi),
        #             'tipologia': tipologia,
        #             'tempi_di_realizzazione' : r['tempistica_prevista'],
        #             'stato_attuale': r['stato_attuale'],
        #             'interventi_previsti':r['interventi_previsti'],
        #             'epoca':r['epoca'],
        #             'cenni_storici':r['cenni_storici'],
        #             'ulteriori_info':r['ulteriori_informazioni'],
        #             'slug': slugify(r['denominazione'][:50]+r['id_progetto']),
        #             }
        #     )
        #
        #     if options['update']:
        #         progetto.territorio=territorio
        #         progetto.importo_previsto=importo_previsto
        #         progetto.riepilogo_importi= Decimal(riepilogo_importi)
        #         progetto.tipologia = tipologia
        #         progetto.tempi_di_realizzazione = r['tempistica_prevista']
        #         progetto.stato_attuale = r['stato_attuale']
        #         progetto.interventi_previsti = r['interventi_previsti']
        #         progetto.epoca = r['epoca']
        #         progetto.cenni_storici = r['cenni_storici']
        #         progetto.ulteriori_info = r['ulteriori_informazioni']
        #         progetto.ubicazione = r['ubicazione']
        #
        #         updated=True
        #         progetto.save()
        #
        #     if created:
        #         self.logger.info("%s: progetto inserito: %s" % ( c, progetto))
        #     else:
        #         if updated:
        #             self.logger.debug("%s: progetto trovato e aggiornato: %s" % (c, progetto))
        #         else:
        #             self.logger.debug("%s: progetto trovato e non aggiornato: %s" % (c, progetto))
        #
        #     c += 1
