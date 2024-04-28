from django.db import models
from accounts.models.user import User



class CoachProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="coach")
    image = models.ImageField(upload_to="coach_img", default="coach_img/default.png")
    cover = models.ImageField(upload_to="coach_cover", default="coach_cover/default.png")
    bio = models.TextField(max_length=5000,blank=True,null=True)
    gender_choices = (("male", "male"), ("female", "female"))
    gender = models.CharField(choices=gender_choices, default="male", max_length=128)
    instagram = models.CharField(max_length=256,blank=True,null=True)
    whatsapp = models.CharField(max_length=256,blank=True,null=True)
    telegram = models.CharField(max_length=256,blank=True,null=True)

    class Meta:
        verbose_name = "coach profile"
        verbose_name_plural = "coach profiles"

    def __str__(self):
        return self.user.phone_number




class Certificate(models.Model):
    user = models.ForeignKey(CoachProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=256,null=True,blank=True)
    image = models.ImageField(upload_to="certificate")
    date = models.CharField(max_length=128,null=True,blank=True)

    def __str__(self):
        return self.title




class Gallery(models.Model):
    user = models.ForeignKey(CoachProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=256,null=True,blank=True)
    image = models.ImageField(upload_to="certificate")
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

