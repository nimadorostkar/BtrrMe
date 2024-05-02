from django.db import models
from accounts.models import User, CoachProfile
from ckeditor.fields import RichTextField
from django.db.models.signals import pre_save
from config.utils import unique_slug_generator


class PostComment(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.sender)



class Category(models.Model):
    name = models.CharField(max_length=255,unique=True)

    def __str__(self):
        return str(self.name)



class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,null=True,blank=True,unique=True)
    author = models.ForeignKey(CoachProfile, on_delete=models.CASCADE)
    cover = models.ImageField(upload_to='blog_cover', default="blog_cover/default.png")
    body = RichTextField(blank=False,null=True)
    comments = models.ManyToManyField(PostComment,blank=True)
    post_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category,null=True,blank=True,on_delete=models.PROTECT)

    def __str__(self):
        return self.title + ' | ' + str(self.author)

def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_generator, sender=Post)



