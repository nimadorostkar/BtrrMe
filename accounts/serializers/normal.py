from rest_framework import serializers
from accounts.models import BodyVersion
from accounts.serializers import UserFullProfileSerializer

class BodyVersionSerializer(serializers.ModelSerializer):
    user = UserFullProfileSerializer(read_only=True)
    class Meta:
        model = BodyVersion
        fields = '__all__'
