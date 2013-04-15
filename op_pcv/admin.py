from models import Parlamentare,GruppoParlamentare, Entry
from django.contrib import admin


class ParlamentareAdmin(admin.ModelAdmin):
    ordering = ('cognome',)
    list_filter = ('ramo_parlamento','gruppo_parlamentare','adesione','in_carica')
    search_fields = ['^nome', '^cognome']


class GruppoParlamentareAdmin(admin.ModelAdmin):
    pass

class EntryAdmin(admin.ModelAdmin):
    ordering = ('published_at',)
    list_filter = ('published','colonna',)
    search_fields = ['^title']


admin.site.register(Parlamentare, ParlamentareAdmin)
admin.site.register(GruppoParlamentare, GruppoParlamentareAdmin)
admin.site.register(Entry, EntryAdmin)

