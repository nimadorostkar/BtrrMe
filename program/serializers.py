from program.models import Program, Program_payment, Supplement_program, Nutrition_program, Workout_program
from rest_framework import serializers
from accounts.serializers import CoachFullProfileSerializer,UserFullProfileSerializer,BodyVersionSerializer
from accounts.models import BodyVersion
from program.models import Nutrition_program, Nutrition_program_table
from nutrition.serializers import NutritionSerializer

class Workout_programSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout_program
        fields = "__all__"


class NutritionProgramTableSerializer(serializers.ModelSerializer):
    nutrition = NutritionSerializer()
    class Meta:
        model = Nutrition_program_table
        fields = "__all__"


class Supplement_programSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplement_program
        fields = "__all__"


class Nutrition_programSerializer(serializers.ModelSerializer):
    nutrition_program_table = serializers.SerializerMethodField()
    def get_nutrition_program_table(self, obj):
        nutrition_table = Nutrition_program_table.objects.filter(nutrition_program=obj)
        return NutritionProgramTableSerializer(nutrition_table,many=True).data
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


class FullProgramWithMetricSerializer(serializers.ModelSerializer):
    user = UserFullProfileSerializer()
    coach = CoachFullProfileSerializer()
    payment = Program_paymentSerializer()
    supplement_program = Supplement_programSerializer()
    nutrition_program = Nutrition_programSerializer()
    workout_program = Workout_programSerializer()
    version = serializers.SerializerMethodField()

    def get_version(self,obj):
        version = BodyVersion.objects.filter(user=obj.user).latest('created_at')
        return BodyVersionSerializer(version).data
    class Meta:
        model = Program
        #fields = ('user', 'version')
        fields = "__all__"


