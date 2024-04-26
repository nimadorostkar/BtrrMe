from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models.user import User


class CoachProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="coach")
    bio = models.CharField(max_length=5000,blank=True,null=True)

    class Meta:
        verbose_name = "coach profile"
        verbose_name_plural = "coach profiles"

    def __str__(self):
        return self.user.phone_number


'''
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        CoachProfile.objects.create(user=instance)
'''