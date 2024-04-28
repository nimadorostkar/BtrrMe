from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from blog.serializers import PostSerializer
from blog.models import Post,Category,PostComment
from rest_framework.permissions import AllowAny
from accounts.views.permissions import IsCoach, IsNormal
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import GenericAPIView


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100




class PostList(GenericAPIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['post_date', 'category', 'author']
    search_fields = ['title', 'body', 'slug']
    ordering_fields = ['post_date', 'category', 'author']

    def get(self, *args, **kwargs):
        posts = self.filter_queryset(Post.objects.all())
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.filter_queryset(Post.objects.all())
        return Response(serializer.data, status=status.HTTP_200_OK)




class PostItem(APIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
    def get(self, *args, **kwargs):
        try:
            post = Post.objects.get(slug=self.kwargs["slug"])
            serializer = self.serializer_class(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("Post not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)

