from django.db import models
from ckeditor.fields import RichTextField
from workout.models.muscle import Muscle


class Equipment(models.Model):
    name = models.CharField(max_length=128,unique=True)
    image = models.ImageField(upload_to="media/equipment",default="media/equipment/default.png")

    def __str__(self):
        return str(self.name)



class Workout(models.Model):
    place_choices = (("تمرین در منزل", "تمرین در منزل"), ("تمرین در باشگاه", "تمرین در باشگاه"))
    motion_status_choices = (("خوابیده", "خوابیده"), ("ایستاده", "ایستاده"), ("نشسته", "نشسته"), ("ترکیبی", "ترکیبی"))
    type_choices = (("هوازی", "هوازی"), ("کششی", "کششی"), ("کار با وزنه", "کار با وزنه"), ("وزن بدن", "وزن بدن"))
    gender_choices = (("male", "male"),("female","female"),("all", "all"))
    hardness_choices = (("آسان", "آسان"), ("متوسط", "متوسط"), ("سخت", "سخت"))

    name = models.CharField(max_length=256,unique=True)
    english_name = models.CharField(max_length=256, unique=True, null=True, blank=True)
    description = RichTextField(max_length=5000,null=True,blank=True)
    muscle = models.ForeignKey(Muscle,on_delete=models.CASCADE)
    place = models.CharField(choices=place_choices, default="تمرین در باشگاه", max_length=128)
    motion_status = models.CharField(choices=motion_status_choices, default="ترکیبی", max_length=128)
    type = models.CharField(choices=type_choices, default="کار با وزنه", max_length=128)
    equipment = models.ManyToManyField(Equipment)
    gender = models.CharField(choices=gender_choices, default="all", max_length=128)
    hardness = models.CharField(choices=hardness_choices, default="all", max_length=128)
    image = models.FileField(upload_to="media/workout",default="media/workout/default.png")
    video_url = models.URLField(null=True, blank=True)
    video = models.FileField(upload_to="media/workout_video",null=True,blank=True)

    def __str__(self):
        return str(self.name)
