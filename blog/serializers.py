from blog.models import Post,PostComment,Category
from rest_framework import serializers
from accounts.serializers import CoachFullProfileSerializer


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = "__all__"

class PostDetailSerializer(serializers.ModelSerializer):
    author = CoachFullProfileSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    comments = PostCommentSerializer(read_only=True, many=True)
    class Meta:
        model = Post
        fields = "__all__"
