from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from program.serializers import ProgramSerializer,FullProgramSerializer,Program_paymentSerializer, \
    FullProgramWithMetricSerializer, Nutrition_programSerializer
from program.models import Program,Program_payment, Nutrition_program, Nutrition_program_table
from rest_framework.permissions import AllowAny
from accounts.views.permissions import IsCoach, IsNormal
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import GenericAPIView
from accounts.serializers import UserSerializer, UserProfileSerializer, BodyVersionSerializer, BodyVersionCreatSerializer
from accounts.models import User, UserProfile, BodyVersion, CoachProfile
from django.db.models import Q
from django.shortcuts import get_object_or_404
from nutrition.serializers import NutritionSerializer
from nutrition.models import Nutrition


class NutritionProgram(APIView):
    serializer_class = Nutrition_programSerializer
    permission_classes = [IsCoach]
    def get(self, *args, **kwargs):
        coach = CoachProfile.objects.get(user=self.request.user)
        program = Program.objects.get(id=self.kwargs["id"])

        program_permission = Program.objects.filter(
            Q(user=program.user,coach=coach,status="completed") |
            Q(user=program.user,coach=coach,status="new-and-payment-pending") |
            Q(user=program.user, coach=coach, status="paid-and-waiting-for-program"))

        if program_permission:
            serializer = self.serializer_class(program.nutrition_program)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("you don't have permission to this user data.", status=status.HTTP_406_NOT_ACCEPTABLE)


    def post(self, *args, **kwargs):
        coach = CoachProfile.objects.get(user=self.request.user)
        program = Program.objects.get(id=self.kwargs["id"])

        program_permission = Program.objects.filter(
            Q(user=program.user, coach=coach, status="completed") |
            Q(user=program.user, coach=coach, status="new-and-payment-pending") |
            Q(user=program.user, coach=coach, status="paid-and-waiting-for-program"))

        if program_permission:

            data = self.request.data
            print(data)

            nutrition_program = Nutrition_program()
            nutrition_program.description = data['description']
            nutrition_program.save()

            for obj in data['nutrition_program_table']:
                nutrion_table = Nutrition_program_table()
                nutrion_table.nutrition_program = nutrition_program
                nutrion_table.nutrition = Nutrition.objects.get(id=obj['nutrition'])
                nutrion_table.qty = obj['qty']
                nutrion_table.time = obj['time']
                nutrion_table.save()

            program.nutrition_program = nutrition_program
            program.save()

            return Response("oooo", status=status.HTTP_200_OK)
        else:
            return Response("you don't have permission to this user data.", status=status.HTTP_406_NOT_ACCEPTABLE)







