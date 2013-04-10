from models import Parlamentare
from django.contrib import admin


class ParlamentareAdmin(admin.ModelAdmin):

    search_fields = ['^nome', '^cognome']


admin.site.register(Parlamentare, ParlamentareAdmin)


