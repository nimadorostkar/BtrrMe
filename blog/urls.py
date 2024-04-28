from django.urls import path
from blog.views import PostList, PostItem

urlpatterns = [
    path("posts", PostList.as_view(), name="posts"),
    path('post-item/<str:slug>', PostItem.as_view(), name='post-item'),
]