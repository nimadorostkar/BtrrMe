from blog.models import Post,PostComment,Category
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"