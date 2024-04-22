from django.urls import path
from nutrition.views import NutritionList

urlpatterns = [
    path("list", NutritionList.as_view(), name="list"),
]