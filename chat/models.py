from django.db import models
from accounts.models import User


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=255,null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    room_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user}: {self.content}"