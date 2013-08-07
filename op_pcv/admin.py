from django.contrib.admin import SimpleListFilter
from models import Parlamentare,GruppoParlamentare, Entry
import csv
from django.http import HttpResponse
from django.contrib import admin

def export_select_fields_csv_action(description="Export selected objects as CSV file",
                                    fields=None, exclude=None, header=True):
    """
    This function returns an export csv action

    'fields' is a list of tuples denoting the field and label to be exported. Labels
    make up the header row of the exported file if header=True.

        fields=[
                ('field1', 'label1'),
                ('field2', 'label2'),
                ('field3', 'label3'),
            ]

    'exclude' is a flat list of fields to exclude. If 'exclude' is passed,
    'fields' will not be used. Either use 'fields' or 'exclude.'

        exclude=['field1', 'field2', field3]

    'header' is whether or not to output the column names as the first row

    Based on: http://djangosnippets.org/snippets/2020/
    """
    def export_as_csv(modeladmin, request, queryset):
        """
        Generic csv export admin action.
        based on http://djangosnippets.org/snippets/1697/
        """
        opts = modeladmin.model._meta
        field_names = [field.name for field in opts.fields]
        labels = []
        if exclude:
            field_names = [v for v in field_names if v not in exclude]
        elif fields:
            field_names = [k for k, v in fields if k in field_names]
            labels = [v for k, v in fields if k in field_names]

        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(opts).replace('.', '_')

        writer = csv.writer(response)
        if header:
            if labels:
                writer.writerow(labels)
            else:
                writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([unicode(getattr(obj, field)).encode('utf-8') for field in field_names])
        return response
    export_as_csv.short_description = description
    return export_as_csv



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
    list_filter = ('ramo_parlamento','gruppo_parlamentare','adesione',HasTwitterFilter,'in_carica','big', 'capogruppo', 'presidente_commissione','firmatario_testo')
    search_fields = ['^nome', '^cognome']
    actions = [
        export_select_fields_csv_action("Esporta elementi selezionati in un file CSV",
                             fields=[
                                 ('nome', 'Nome'),
                                 ('cognome', 'Cognome'),
                                 ('gruppo_parlamentare', 'Gruppo'),
                                 ('account_mail', 'Email'),
                                 ],
                             header=True
        ),
        ]

class GruppoParlamentareAdmin(admin.ModelAdmin):
    pass

class EntryAdmin(admin.ModelAdmin):
    ordering = ('published_at',)
    list_filter = ('published','colonna',)
    search_fields = ['^title']


admin.site.register(Parlamentare, ParlamentareAdmin)
admin.site.register(GruppoParlamentare, GruppoParlamentareAdmin)
admin.site.register(Entry, EntryAdmin)

