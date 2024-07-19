from django.db import models
from django.utils.html import format_html


class Nutrition(models.Model):
    amount_choices = (("one","one"), ("100g","100g"))
    name = models.CharField(max_length=128,unique=True)
    english_name = models.CharField(max_length=128, unique=True)
    amount = models.CharField(max_length=20, default="100g", choices=amount_choices)
    protein = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    carbo = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    sugar = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    fat = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    fiber = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    calorie = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    img = models.URLField(null=True,blank=True)

    def __str__(self):
        return str(self.name) +' | '+ str(self.amount) +' | '+ str(self.calorie)

    def image(self):
        return format_html("<img width=40 src='{}'>".format(self.img))
