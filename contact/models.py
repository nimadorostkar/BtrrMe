from django.db import models


class Contact(models.Model):
    status_type = (("new", "new"), ("checked", "checked"))
    status = models.CharField(max_length=15, default="new", choices=status_type)
    title = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    body = models.TextField(max_length=100000,blank=False,null=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title + ' | ' + str(self.create_at)
