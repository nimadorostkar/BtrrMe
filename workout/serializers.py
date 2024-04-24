from workout.models import Workout
from rest_framework import serializers


class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = "__all__"