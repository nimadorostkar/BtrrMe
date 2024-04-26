from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models.user import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user")
    bio = models.CharField(max_length=5000,blank=True,null=True)

    class Meta:
        verbose_name = "user profile"
        verbose_name_plural = "user profiles"

    def __str__(self):
        return self.user.phone_number

'''
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
'''