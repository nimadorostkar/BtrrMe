from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "username", "user_type", "phone_number", "email", "first_name", "last_name", "birth_date", "is_profile_fill")


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "birth_date", "username")




'''

class UserAllFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = "__all__"






class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("email", "first_name")
        extra_kwargs = {
            "email": {"required": False},
            "first_name": {"required": True},
        }

'''
