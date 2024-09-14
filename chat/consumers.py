import json
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.models import Message
from chat.serializers import ChatMessageSerializer
from asgiref.sync import sync_to_async
from accounts.models import User
from channels.db import database_sync_to_async



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope['user'].is_anonymous:
            await self.close()

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope['user']
        #user = text_data_json['user']

        await self.save_message(user, message, self.room_name)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
                #'user': user
            }
        )

    @database_sync_to_async
    def save_message(self, user, message, room_name):
        #user_obj = User.objects.get(id=user)
        new_message = Message(user=user, content=message, room_name=room_name)
        new_message.save()


    async def chat_message(self, event):
        message = event['message']
        #user = event['user']

        await self.send(text_data=json.dumps({
            'message': message
            #'user': user
        }))