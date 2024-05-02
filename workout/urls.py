from django.urls import path
from workout.views import WorkoutList, WorkoutItem

urlpatterns = [
    path("list", WorkoutList.as_view(), name="list"),
    path('workout-item/<int:id>', WorkoutItem.as_view(), name='workout-item'),
]