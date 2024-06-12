from program.models import Program, Program_payment, Supplement_program, Nutrition_program, Workout_program
from rest_framework import serializers
from accounts.serializers import CoachFullProfileSerializer,UserFullProfileSerializer


class Workout_programSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout_program
        fields = "__all__"


class Supplement_programSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplement_program
        fields = "__all__"

class Nutrition_programSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nutrition_program
        fields = "__all__"


class Program_paymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program_payment
        fields = "__all__"


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = "__all__"


class FullProgramSerializer(serializers.ModelSerializer):
    user = UserFullProfileSerializer()
    coach = CoachFullProfileSerializer()
    payment = Program_paymentSerializer()
    supplement_program = Supplement_programSerializer()
    nutrition_program = Nutrition_programSerializer()
    workout_program = Workout_programSerializer()
    class Meta:
        model = Program
        fields = "__all__"


