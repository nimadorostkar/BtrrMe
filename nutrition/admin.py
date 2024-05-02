from django.contrib import admin
from nutrition.models import Nutrition
from import_export.admin import ImportExportModelAdmin


class NutritionAdmin(ImportExportModelAdmin):
    list_display = ('name', 'amount', 'protein', 'carbo', 'fat', 'calorie')
admin.site.register(Nutrition, NutritionAdmin)

