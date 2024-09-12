from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from chat.serializers import ChatMessageSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets
from chat.models import ChatMessage
import logging

logger = logging.getLogger(__name__)

class ChatMessageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer

    def create(self, request, *args, **kwargs):
        logger.debug(f"Received POST request: {request.data}")
        return super().create(request, *args, **kwargs)