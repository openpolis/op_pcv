from models import Parlamentare
from django.contrib import admin


class ParlamentareAdmin(admin.ModelAdmin):
    list_filter = ('gruppo_parlamentare','adesione')
    search_fields = ['^nome', '^cognome']


admin.site.register(Parlamentare, ParlamentareAdmin)


