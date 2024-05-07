from django.contrib.auth import get_user_model
from rest_framework import serializers
from accounts.models import CoachProfile,UserProfile,Gallery,Certificate


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


class CoachFullProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = CoachProfile
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserFullProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = UserProfile
        fields = '__all__'

class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = '__all__'