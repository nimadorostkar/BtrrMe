from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from chat.serializers import ChatMessageSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets
from chat.models import Message
from accounts.models import User, UserProfile, CoachProfile
from django.db.models import Q


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
    def post(self, *args, **kwargs):
        try:
            data = self.request.data
            data["room_name"] = self.kwargs["room_name"]
            data["user"] = self.request.user.id
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("Something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)


class RoomListViewSet(APIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]
    def get(self, *args, **kwargs):
        try:
            #room_names = Message.objects.filter(user=self.request.user).values_list('room_name', flat=True).distinct()
            query = Q()
            query |= Q(room_name__contains=str(self.request.user.id))
            room_names = Message.objects.filter(query).values_list('room_name', flat=True).distinct()

            rooms = []
            for item in room_names:
                coach_id, user_id = item.split('_')
                if self.request.user.user_type == "coach":
                    usr = User.objects.get(id=int(user_id))
                    usr_profile = UserProfile.objects.get(user=usr)
                    room = {"room_name":item,"first_name":usr.first_name,"last_name":usr.last_name,"image":usr_profile.image.url}
                elif self.request.user.user_type == "normal":
                    usr = User.objects.get(id=int(coach_id))
                    coach_profile = CoachProfile.objects.get(user=usr)
                    room = {"room_name":item,"first_name": usr.first_name, "last_name": usr.last_name, "image": coach_profile.image.url}
                else:
                    room = {"room_name":" ", "first_name": " ", "last_name": " ", "image": " "}
                rooms.append(room)
            return Response(rooms, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"Rooms not found or something went wrong. {e}", status=status.HTTP_400_BAD_REQUEST)
