from django.contrib import admin
from contact.models import Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = ('title', 'create_at', 'status')
admin.site.register(Contact, ContactAdmin)

