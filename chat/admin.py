from django.contrib import admin
from chat.models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ('user','room_name','timestamp')
admin.site.register(Message, MessageAdmin)

