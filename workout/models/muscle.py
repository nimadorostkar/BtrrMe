from django.db import models


class MainMuscle(models.Model):
    name = models.CharField(max_length=256,unique=True)
    english_name = models.CharField(max_length=256, unique=True, null=True, blank=True)
    description = models.TextField(blank=True,null=True)
    image = models.ImageField(upload_to="media/main_muscle",default="media/main_muscle/default.png")

    def __str__(self):
        return str(self.name) +" | "+ str(self.english_name)


class Muscle(models.Model):
    main_muscle = models.ForeignKey(MainMuscle, on_delete=models.CASCADE)
    name = models.CharField(max_length=256,unique=True)
    english_name = models.CharField(max_length=256, unique=True, null=True, blank=True)
    description = models.TextField(blank=True,null=True)
    image = models.ImageField(upload_to="media/muscle",default="media/muscle/default.png")

    def __str__(self):
        return str(self.name) +" | "+ str(self.english_name)

