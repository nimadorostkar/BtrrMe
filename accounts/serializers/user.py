from django.contrib.auth import get_user_model
from rest_framework import serializers
from accounts.models import CoachProfile,UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "username", "user_type", "phone_number", "email", "first_name", "last_name", "age", "is_profile_fill")


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "age", "username")


class CoachProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoachProfile
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'