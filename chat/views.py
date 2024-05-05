from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from chat.serializers import ChatSerializer,MessageSerializer
from chat.models import Chat,Message
from rest_framework.permissions import AllowAny
from django.db.models import Q


class UserChatList(APIView):
    permission_classes = [AllowAny]
    serializer_class = ChatSerializer
    def get(self, *args, **kwargs):
        try:
            chats = Chat.objects.filter(Q(user1=self.request.user)|Q(user2=self.request.user))
            serializer = self.serializer_class(chats,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("Chats not found or something went wrong, try again",status=status.HTTP_400_BAD_REQUEST)



class StartChat(APIView):
    permission_classes = [AllowAny]
    serializer_class = ChatSerializer
    def post(self, *args, **kwargs):
        try:
            chats = Chat.objects.filter(Q(user1=self.request.user)|Q(user2=self.request.user))
            serializer = self.serializer_class(chats,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("Chats not found or something went wrong, try again",status=status.HTTP_400_BAD_REQUEST)


