from program.models import Program, Transaction, Supplement_program, Nutrition_program, Workout_program
from rest_framework import serializers
from accounts.serializers import CoachFullProfileSerializer,UserFullProfileSerializer,BodyVersionSerializer
from accounts.models import BodyVersion
from program.models import Nutrition_program, Nutrition_program_table, Supplement_program_table
from nutrition.serializers import NutritionSerializer
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from supplement.serializers import SupplementSerializer


class Workout_programSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout_program
        fields = "__all__"


class NutritionProgramTableSerializer(serializers.ModelSerializer):
    nutrition = NutritionSerializer()
    class Meta:
        model = Nutrition_program_table
        fields = "__all__"


class Supplement_program_tableSerializer(serializers.ModelSerializer):
    supplement = SupplementSerializer()
    class Meta:
        model = Supplement_program_table
        fields = "__all__"


class Supplement_programSerializer(serializers.ModelSerializer):
    supplement_program_table = serializers.SerializerMethodField()
    def get_supplement_program_table(self, obj):
        supplement_table = Supplement_program_table.objects.filter(supplement_program=obj)
        return Supplement_program_tableSerializer(supplement_table, many=True).data
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


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = "__all__"


class FullProgramSerializer(serializers.ModelSerializer):
    user = UserFullProfileSerializer()
    coach = CoachFullProfileSerializer()
    payment = TransactionSerializer()
    supplement_program = Supplement_programSerializer()
    nutrition_program = Nutrition_programSerializer()
    workout_program = Workout_programSerializer()
    class Meta:
        model = Program
        fields = "__all__"


class FullProgramWithMetricSerializer(serializers.ModelSerializer):
    user = UserFullProfileSerializer()
    coach = CoachFullProfileSerializer()
    payment = TransactionSerializer()
    supplement_program = Supplement_programSerializer()
    nutrition_program = Nutrition_programSerializer()
    workout_program = Workout_programSerializer()
    version = serializers.SerializerMethodField()

    def get_version(self,obj):
        body_versions = BodyVersion.objects.filter(user=obj.user)
        if not body_versions.exists():
            get_object_or_404(BodyVersion)
        latest_body_version = body_versions.latest('created_at')
        return BodyVersionSerializer(latest_body_version).data


    class Meta:
        model = Program
        #fields = ('user', 'version')
        fields = "__all__"

