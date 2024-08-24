from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from contact.serializers import ContactSerializer
from rest_framework.permissions import AllowAny


class AddContact(APIView):
    serializer_class = ContactSerializer
    permission_classes = [AllowAny]

    def post(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)