from django.urls import re_path
from chat import consumers


websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/chat/user/(?P<user_id>\w+)/$', consumers.UserChatConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<user1>\w+)/(?P<user2>\w+)/$', consumers.UsersChatConsumer.as_asgi()),
]
