from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.serializers import UserSerializer, UserUpdateSerializer
from rest_framework.permissions import IsAuthenticated
from accounts.models import User



class Profile(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        serializer = self.serializer_class(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, *args, **kwargs):
        profile = User.objects.get(id=self.request.user.id)
        serializer = UserUpdateSerializer(profile, data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
