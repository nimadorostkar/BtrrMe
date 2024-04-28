from django.contrib import admin
from blog.models import PostComment,Category,Post


class PostCommentAdmin(admin.ModelAdmin):
    list_display = ('sender', 'create_at')
admin.site.register(PostComment, PostCommentAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Category, CategoryAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'category', 'post_date')
admin.site.register(Post, PostAdmin)