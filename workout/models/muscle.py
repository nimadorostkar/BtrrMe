from django.db import models


class MainMuscle(models.Model):
    name = models.CharField(max_length=128,unique=True)
    description = models.TextField(blank=True,null=True)
    image = models.ImageField(upload_to="main_muscle",default="main_muscle/default.png")

    def __str__(self):
        return str(self.name)



class Muscle(models.Model):
    main_muscle = models.ForeignKey(MainMuscle, on_delete=models.CASCADE)
    name = models.CharField(max_length=128,unique=True)
    description = models.TextField(blank=True,null=True)
    image = models.ImageField(upload_to="muscle",default="muscle/default.png")

    def __str__(self):
        return str(self.name)