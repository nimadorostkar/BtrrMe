from django.db import models
from accounts.models.user import User
from decimal import Decimal


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user")
    bio = models.CharField(max_length=5000,blank=True,null=True)
    image = models.ImageField(upload_to="media/user_img", default="media/user_img/default.png")
    gender_choices = (("male", "male"), ("female", "female"))
    gender = models.CharField(choices=gender_choices, default="male", max_length=128)
    height = models.IntegerField(default=100)
    injury = models.CharField(max_length=5000,blank=True,null=True)
    class Meta:
        verbose_name = "user profile"
        verbose_name_plural = "user profiles"
    def __str__(self):
        return str(self.user.phone_number)



def img_path(instance, filename):
    return 'body_version/{0}/{1}'.format(instance.user.user.phone_number, filename)


def calculate_bmr_and_tdee(weight, height, age, gender, activity_type):
    if gender == "male":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    elif gender == "female":
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    else:
        bmr = 0
    if activity_type == "کم تحرک (کمی یا بدون ورزش)":
        tdee = bmr * 1.2
    elif activity_type == "کم تحرک (ورزش سبک 1 تا 3 ساعت در هفته)":
        tdee = bmr * 1.375
    elif activity_type == "فعالیت متوسط (۳ الی ۵ ساعت در هفته)":
        tdee = bmr * 1.55
    elif activity_type == "بسیار فعال (۶ الی ۷ ساعت در هفته)":
        tdee = bmr * 1.725
    elif activity_type == "فعالیت بسیار بالا (فعالیت سخت ورزشی و کاری)":
        tdee = bmr * 1.9
    else:
        tdee = 0
    print(tdee)
    return tdee


class BodyVersion(models.Model):
    CHOICES = (("کم تحرک (کمی یا بدون ورزش)", "کم تحرک (کمی یا بدون ورزش)"),
               ("کم تحرک (ورزش سبک 1 تا 3 ساعت در هفته)", "کم تحرک (ورزش سبک 1 تا 3 ساعت در هفته)"),
               ("فعالیت متوسط (۳ الی ۵ ساعت در هفته)", "فعالیت متوسط (۳ الی ۵ ساعت در هفته)"),
               ("بسیار فعال (۶ الی ۷ ساعت در هفته)", "بسیار فعال (۶ الی ۷ ساعت در هفته)"),
               ("فعالیت بسیار بالا (فعالیت سخت ورزشی و کاری)", "فعالیت بسیار بالا (فعالیت سخت ورزشی و کاری)"),)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    weight = models.DecimalField(default=1,max_digits=5,decimal_places=2,verbose_name="وزن")
    arm_circumference = models.DecimalField(default=1,max_digits=5,decimal_places=2,verbose_name="دور بازو")
    forehand_circumference = models.DecimalField(default=1,max_digits=5,decimal_places=2,verbose_name="دور ساعد")
    chest_circumference = models.DecimalField(default=1,max_digits=5,decimal_places=2,verbose_name="دور سینه")
    stomach_circumference = models.DecimalField(default=1,max_digits=5,decimal_places=2,verbose_name="دور شکم")
    waist_circumference = models.DecimalField(default=1,max_digits=5,decimal_places=2,verbose_name="دور کمر")
    hip_circumference = models.DecimalField(default=1,max_digits=5,decimal_places=2,verbose_name="دور باسن")
    thigh_circumference = models.DecimalField(default=1,max_digits=5,decimal_places=2,verbose_name="دور ران")
    leg_circumference = models.DecimalField(default=1,max_digits=5,decimal_places=2,verbose_name="دور ساق")
    front_double_biceps = models.ImageField(upload_to=img_path, default="media/body_version/default.png")
    back_double_biceps = models.ImageField(upload_to=img_path, default="media/body_version/default.png")
    front_normal = models.ImageField(upload_to=img_path, default="media/body_version/default.png")
    back_normal = models.ImageField(upload_to=img_path, default="media/body_version/default.png")
    left_side = models.ImageField(upload_to=img_path, default="media/body_version/default.png")
    right_side = models.ImageField(upload_to=img_path, default="media/body_version/default.png")
    in_body_file = models.FileField(upload_to=img_path,null=True,blank=True)
    medical_checkup_file = models.FileField(upload_to=img_path,null=True,blank=True)
    description = models.CharField(max_length=4000,blank=True,null=True)
    activity_type = models.CharField(choices=CHOICES, default="فعالیت متوسط (۳ الی ۵ ساعت در هفته)", max_length=256)
    created_at = models.DateField(auto_now_add=True)
    BMI = models.DecimalField(default=0,max_digits=5,decimal_places=2)
    WHR = models.DecimalField(default=0,max_digits=5,decimal_places=2)
    BMR = models.DecimalField(default=0,max_digits=6,decimal_places=2)
    def __str__(self):
        return str(self.user) + " | " + str(self.created_at)

    def save(self, *args, **kwargs):
        height_m = (self.user.height/100)
        self.BMI = self.weight / Decimal(str((height_m * height_m)))

        height = self.user.height
        gender = self.user.gender
        age = self.user.user.age
        weight = float(self.weight)
        activity_type = self.activity_type
        self.BMR = calculate_bmr_and_tdee(weight, height, age, gender, activity_type)

        self.WHR = self.waist_circumference / self.hip_circumference
        super(BodyVersion, self).save()