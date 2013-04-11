from models import Parlamentare,GruppoParlamentare
from django.contrib import admin


class ParlamentareAdmin(admin.ModelAdmin):
    ordering = ('cognome',)
    list_filter = ('gruppo_parlamentare','adesione','in_carica')
    search_fields = ['^nome', '^cognome','^gruppo_parlamentare']


class GruppoParlamentareAdmin(admin.ModelAdmin):

    pass



admin.site.register(Parlamentare, ParlamentareAdmin)
admin.site.register(GruppoParlamentare, GruppoParlamentareAdmin)


