from supplement.models import Supplement
from rest_framework import serializers


class SupplementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplement
        fields = "__all__"