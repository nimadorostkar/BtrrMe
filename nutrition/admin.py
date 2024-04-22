from django.contrib import admin
from nutrition.models import Nutrition


class NutritionAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'protein', 'carbo', 'fat', 'calorie')
admin.site.register(Nutrition, NutritionAdmin)

