from django.urls import path
from nutrition.views import NutritionList, NutritionItem

urlpatterns = [
    path("list", NutritionList.as_view(), name="list"),
    path('nutrition-item/<int:id>', NutritionItem.as_view(), name='nutrition-item'),
]