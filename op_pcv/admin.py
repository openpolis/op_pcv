from models import Parlamentare,GruppoParlamentare
from django.contrib import admin


class ParlamentareAdmin(admin.ModelAdmin):
    list_filter = ('gruppo_parlamentare','adesione')
    search_fields = ['^nome', '^cognome']

class GruppoParlamentareAdmin(admin.ModelAdmin):

    pass



admin.site.register(Parlamentare, ParlamentareAdmin)
admin.site.register(GruppoParlamentare, GruppoParlamentareAdmin)


