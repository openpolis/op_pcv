from django.contrib.admin import SimpleListFilter
from models import Parlamentare,GruppoParlamentare, Entry
from django.contrib import admin

class HasTwitterFilter(SimpleListFilter):
    title = 'Ha twitter'
    parameter_name = 'has_twitter'

    def lookups(self, request, model_admin):
        return (
            ('1', ('Si')),
            ('0', ('No')),
        )

    def queryset(self, request, queryset):

        if self.value():
            if self.value() == '1':
                return queryset.exclude(account_twitter='')
            else:
                return queryset.filter(account_twitter='')

        else:
            return queryset


class ParlamentareAdmin(admin.ModelAdmin):
    list_per_page = 1100
    ordering = ('cognome',)
    list_filter = ('ramo_parlamento','gruppo_parlamentare','adesione',HasTwitterFilter,'in_carica','big')
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

