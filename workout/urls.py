from django.urls import path
from workout.views import WorkoutList

urlpatterns = [
    path("list", WorkoutList.as_view(), name="list"),
]