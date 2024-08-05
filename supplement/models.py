from django.db import models
from ckeditor.fields import RichTextField



class Supplement(models.Model):
    name = models.CharField(max_length=128,unique=True)
    image = models.ImageField(upload_to="media/supplement", default="media/supplement/default.png")
    description = RichTextField(max_length=5000, null=True, blank=True)

    def __str__(self):
        return str(self.name)
