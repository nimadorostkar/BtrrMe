from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from chat.serializers import ChatMessageSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets
from chat.models import Message


class ChatMessageViewSet(APIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]
    def get(self, *args, **kwargs):
        try:
            message = Message.objects.filter(user=self.request.user)
            serializer = self.serializer_class(message,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("Message not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)


class RoomMessageViewSet(APIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]
    def get(self, *args, **kwargs):
        try:
            message = Message.objects.filter(room_name=self.kwargs["room_name"])
            serializer = self.serializer_class(message,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("Message not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)


class RoomListViewSet(APIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]
    def get(self, *args, **kwargs):
        try:
            room_names = Message.objects.filter(user=self.request.user).values_list('room_name', flat=True).distinct()
            return Response(room_names, status=status.HTTP_200_OK)
        except:
            return Response("Rooms not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)