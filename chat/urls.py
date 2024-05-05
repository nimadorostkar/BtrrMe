from django.urls import path
from chat.views import UserChatList,StartChat


urlpatterns = [
    path("list", UserChatList.as_view(), name="list"),
    path("start", StartChat.as_view(), name="start"),
    #path('workout-item/<int:id>', WorkoutItem.as_view(), name='workout-item'),
]


