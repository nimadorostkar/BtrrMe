from workout.models import Workout, Muscle, Equipment
from rest_framework import serializers

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = "__all__"
class MuscleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Muscle
        fields = "__all__"


class WorkoutSerializer(serializers.ModelSerializer):
    muscle = MuscleSerializer(read_only=True)
    equipment = EquipmentSerializer(many=True, read_only=True)
    class Meta:
        model = Workout
        fields = "__all__"