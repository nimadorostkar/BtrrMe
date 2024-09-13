from django.urls import path
from chat.views import ChatMessageViewSet, RoomMessageViewSet, RoomListViewSet

urlpatterns = [
    path("chat", ChatMessageViewSet.as_view(), name="chat"),
    path("room-list", RoomListViewSet.as_view(), name="room-list"),
    path("room/<str:room_name>", RoomMessageViewSet.as_view(), name="room"),
]
