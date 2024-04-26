from django.contrib import admin
from supplement.models import Supplement


class SupplementAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Supplement, SupplementAdmin)

