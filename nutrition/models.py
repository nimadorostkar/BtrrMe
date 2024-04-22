from django.db import models


class Nutrition(models.Model):
    amount_choices = (("one","one"), ("100g","100g"))
    name = models.CharField(max_length=128,unique=True)
    amount = models.CharField(max_length=20, default="normal", choices=amount_choices)
    protein = models.IntegerField(default=0)
    carbo = models.IntegerField(default=0)
    sugar = models.IntegerField(default=0)
    fat = models.IntegerField(default=0)
    fiber = models.IntegerField(default=0)
    calorie = models.IntegerField(default=0)

    def __str__(self):
        return str(self.name) +' | '+ str(self.amount) +' | '+ str(self.calorie)
