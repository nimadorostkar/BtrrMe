from nutrition.models import Nutrition
from rest_framework import serializers


class NutritionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nutrition
        fields = "__all__"


class NutritionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nutrition
        fields = "__all__"