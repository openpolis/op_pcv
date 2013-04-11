# -*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import connection
from django.db.utils import DatabaseError
from django.core.management.base import BaseCommand, CommandError
from op_pcv import utils
from op_pcv.models import Parlamentare, GruppoParlamentare, UltimoAggiornamento
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
                    help='Type of import: dep|sen|gruppi'),
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
    db_encoding = 'utf-8'
    file_encoding='utf-8'
    logger = logging.getLogger('csvimport')
    unicode_reader = None

    def handle(self, *args, **options):

        self.csv_file = options['csvfile']
        self.logger.info('CSV FILE "%s"\n' % self.csv_file )

        # read first csv file
        try:
            self.unicode_reader = \
                utils.UnicodeDictReader(open(self.csv_file, 'r'), encoding=self.file_encoding, dialect="excel")
        except IOError:
            self.logger.error("It was impossible to open file %s\n" % self.csv_file)
            exit(1)
        except csv.Error, e:
            self.logger.error("CSV error while reading %s: %s\n" % (self.csv_file, e.message))

        if options['type'] == 'dep':
            self.handle_dep(*args, **options)
            UltimoAggiornamento.objects.all().update(data=timezone.now())
        elif options['type'] == 'sen':
            # self.handle_sen(*args, **options)
            UltimoAggiornamento.objects.all().update(data=timezone.now())
        elif options['type'] == 'gruppi':
            self.handle_gruppi(*args, **options)

        else:
            self.logger.error("Wrong type %s. Select among dep, sen, gruppi." % options['type'])
            exit(1)

    def handle_gruppi(self,*args, **options):
        c = 0

        if options['delete']:
            self.logger.info("Erasing the precedently stored data...")
            GruppoParlamentare.objects.all().delete()

        self.logger.info("Inizio import da %s" % self.csv_file)
        for r in self.unicode_reader:
            updated=False
            if r["data_creazione"] is not u"":
                data = r["data_creazione"]
            else:
                data="1970-01-01"

            # metadata nome, sigla, data_creazione
            gruppo, created = GruppoParlamentare.objects.get_or_create(
                nome=r["nome"],

                defaults={
                    'nome':r["nome"],
                    'sigla':r["sigla"].upper(),
                    'data_creazione':data,
                    }
            )
            if created is False and options['update']:
                gruppo.sigla = r['sigla'].upper()
                gruppo.data_creazione=data
                gruppo.save()

                updated=True

            if created:
                self.logger.info("%s: gruppo inserito: %s " % ( c, gruppo))
            else:
                if updated:
                    self.logger.debug("%s: gruppo trovato e aggiornato: %s " % ( c,gruppo))
                else:
                    self.logger.debug("%s: gruppo trovato e non aggiornato: %s " % ( c, gruppo))

            c += 1

    def handle_dep(self, *args, **options):

        c = 0

        if options['delete']:
            self.logger.info("Erasing the precedently stored data...")
            Parlamentare.objects.filter(ramo_parlamento=0).delete()

        self.logger.info("Inizio import da %s" % self.csv_file)

        for r in self.unicode_reader:
            updated=False
            r_gruppo_parlamentare=None
            try:
                r_gruppo_parlamentare = GruppoParlamentare.objects.get(sigla=r['Gruppo'].upper())
            except ObjectDoesNotExist:
                r_gruppo_parlamentare = None

            deputato = r["Deputato"]

            # separa nome e cognome
            nomelist=deputato.split(" ")

            r_cognome=""
            r_nome=""

            # ricrea nome e cognome inserendo spazi quando serve
            for s in nomelist:
                trovato=False
                for character in s:
                    if character.islower():
                        trovato=True
                if trovato is False:
                    if r_cognome =="":
                        r_cognome+=s
                    else:
                        r_cognome+=" "+s
                else:
                    if r_nome =="":
                        r_nome+=s
                    else:
                        r_nome+=" "+s

            self.logger.info("%d:Analizzando record: %s %s - %s" % (c, r_nome, r_cognome, r['Gruppo']))

            r_nome=r_nome.encode(self.db_encoding)
            r_cognome=r_cognome.encode(self.db_encoding)

            if r["Risposta twitter"]:
                risposta_twitter=True
            else:
                risposta_twitter=False

            if r["Lettura mail"]:
                lettura_mail=True
            else:
                lettura_mail=False

            if r["Risposta mail"]:
                risposta_mail=True
            else:
                risposta_mail=False

            # ADESIONE_SELECT = (
            #     ('0', 'Non risponde'),
            #     ('1', 'Aderisce'),
            #     ('2', 'Non aderisce'),
            # )

            if r["Adesione"]:
                str_adesione=r["Adesione"].lower()
                if str_adesione ==u"si" or str_adesione == u"sì":
                    adesione = "1"
                else:
                    adesione = "2"
            else:
                adesione ="0"


            # metadata Deputato,Gruppo,Account twitter,Risposta twitter,Contatto mail,Lettura mail,Risposta mail,Adesione
            parlamentare, created = Parlamentare.objects.get_or_create(
                nome=r_nome,
                cognome=r_cognome,

                defaults={
                    'nome':r_nome,
                    'cognome':r_cognome,
                    'gruppo_parlamentare': r_gruppo_parlamentare,
                    'account_twitter': r["Account twitter"],
                    'risposta_twitter': risposta_twitter,
                    'account_mail': r["Contatto mail"],
                    'lettura_mail': lettura_mail,
                    'risposta_mail': risposta_mail,
                    'ramo_parlamento':'0',
                    'adesione': adesione,
                }
            )
            if created is False and options['update']:
                parlamentare.gruppo_parlamentare=r_gruppo_parlamentare
                parlamentare.account_twitter=r["Account twitter"]
                parlamentare.risposta_twitter=risposta_twitter
                parlamentare.account_mail=r["Contatto mail"]
                parlamentare.lettura_mail=lettura_mail
                parlamentare.risposta_mail=risposta_mail
                parlamentare.ramo_parlamento="0"
                parlamentare.adesione=adesione
                parlamentare.save()

                updated=True

            if created:
                self.logger.info("%s: parlamentare inserito: %s %s" % ( c, parlamentare.cognome, parlamentare.nome))
            else:
                if updated:
                    self.logger.debug("%s: parlamentare trovato e aggiornato: %s %s" % ( c, parlamentare.cognome, parlamentare.nome))
                else:
                    self.logger.debug("%s: parlamentare trovato e non aggiornato: %s %s" % ( c, parlamentare.cognome, parlamentare.nome))

            c += 1




