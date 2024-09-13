from chat.models import Message
from rest_framework import serializers


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'