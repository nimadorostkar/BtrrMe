from django.db import models
from accounts.models.user import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user")
    bio = models.CharField(max_length=5000,blank=True,null=True)
    image = models.ImageField(upload_to="user_img", default="user_img/default.png")
    gender_choices = (("male", "male"), ("female", "female"))
    gender = models.CharField(choices=gender_choices, default="male", max_length=128)
    height = models.IntegerField(default=0)
    injury = models.CharField(max_length=5000,blank=True,null=True)
    class Meta:
        verbose_name = "user profile"
        verbose_name_plural = "user profiles"
    def __str__(self):
        return str(self.user.phone_number)



def img_path(instance, filename):
    return 'body_version/{0}/{1}'.format(instance.user.user.phone_number, filename)
class BodyVersion(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    weight = models.DecimalField(default=0,max_digits=5,decimal_places=2,verbose_name="وزن")
    arm_circumference = models.DecimalField(default=0,max_digits=5,decimal_places=2,verbose_name="دور بازو")
    forehand_circumference = models.DecimalField(default=0,max_digits=5,decimal_places=2,verbose_name="دور ساعد")
    chest_circumference = models.DecimalField(default=0,max_digits=5,decimal_places=2,verbose_name="دور سینه")
    stomach_circumference = models.DecimalField(default=0,max_digits=5,decimal_places=2,verbose_name="دور شکم")
    waist_circumference = models.DecimalField(default=0,max_digits=5,decimal_places=2,verbose_name="دور کمر")
    hip_circumference = models.DecimalField(default=0,max_digits=5,decimal_places=2,verbose_name="دور باسن")
    thigh_circumference = models.DecimalField(default=0,max_digits=5,decimal_places=2,verbose_name="دور ران")
    leg_circumference = models.DecimalField(default=0,max_digits=5,decimal_places=2,verbose_name="دور ساق")
    front_double_biceps = models.ImageField(upload_to=img_path, default="body_version/default.png")
    back_double_biceps = models.ImageField(upload_to=img_path, default="body_version/default.png")
    front_normal = models.ImageField(upload_to=img_path, default="body_version/default.png")
    back_normal = models.ImageField(upload_to=img_path, default="body_version/default.png")
    left_side = models.ImageField(upload_to=img_path, default="body_version/default.png")
    right_side = models.ImageField(upload_to=img_path, default="body_version/default.png")
    in_body_file = models.FileField(upload_to=img_path,null=True,blank=True)
    medical_checkup_file = models.FileField(upload_to=img_path,null=True,blank=True)
    description = models.CharField(max_length=4000,blank=True,null=True)
    created_at = models.DateField(auto_now_add=True)
    def __str__(self):
        return str(self.user) + " | " + str(self.created_at)