from django.contrib import admin
from chat.models import Chat, Message


class ChatAdmin(admin.ModelAdmin):
    list_display = ('user1','user2')
admin.site.register(Chat, ChatAdmin)

class MessageAdmin(admin.ModelAdmin):
    list_display = ('chat','user','time')
admin.site.register(Message, MessageAdmin)