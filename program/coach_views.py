from program.serializers import ProgramSerializer,FullProgramSerializer,Program_paymentSerializer, FullProgramWithMetricSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from program.serializers import ProgramSerializer, FullProgramSerializer, Program_paymentSerializer
from program.models import Program, Program_payment
from rest_framework.permissions import AllowAny
from accounts.views.permissions import IsCoach, IsNormal
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import GenericAPIView
from accounts.serializers import UserSerializer, UserProfileSerializer, BodyVersionSerializer, \
    BodyVersionCreatSerializer
from accounts.models import User, UserProfile, BodyVersion, CoachProfile
from django.db.models import Q


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class CoachProgramsList(GenericAPIView):
    permission_classes = [IsCoach]
    pagination_class = CustomPagination
    serializer_class = FullProgramSerializer
    queryset = Program.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'type', 'created_at', 'updated_at','coach']
    search_fields = ['status', 'type', 'description', 'target']
    ordering_fields = ['created_at', 'updated_at', 'duration_day', 'coach']

    def get(self, *args, **kwargs):
        coach = CoachProfile.objects.get(user=self.request.user)
        coach_program = Program.objects.filter(coach=coach)
        programs = self.filter_queryset(coach_program)
        page = self.paginate_queryset(programs)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.filter_queryset(coach_program)
        return Response(serializer.data, status=status.HTTP_200_OK)




class CoachProgramsShortList(GenericAPIView):
    permission_classes = [IsCoach]
    pagination_class = CustomPagination
    serializer_class = ProgramSerializer
    queryset = Program.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'type', 'created_at', 'updated_at','coach']
    search_fields = ['status', 'type', 'description', 'target']
    ordering_fields = ['created_at', 'updated_at', 'duration_day', 'coach']

    def get(self, *args, **kwargs):
        coach = CoachProfile.objects.get(user=self.request.user)
        coach_program = Program.objects.filter(coach=coach)
        programs = self.filter_queryset(coach_program)
        page = self.paginate_queryset(programs)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.filter_queryset(coach_program)
        return Response(serializer.data, status=status.HTTP_200_OK)



class UserLastBodyVersion(APIView):
    serializer_class = BodyVersionSerializer
    permission_classes = [IsCoach]
    def get(self, *args, **kwargs):
        coach = CoachProfile.objects.get(user=self.request.user)
        profile = UserProfile.objects.get(id=self.kwargs["id"])

        program = Program.objects.filter(
            Q(user=profile,coach=coach,status="completed") |
            Q(user=profile,coach=coach,status="new-and-payment-pending") |
            Q(user=profile, coach=coach, status="paid-and-waiting-for-program"))

        if program:
            body_versions = BodyVersion.objects.filter(user=profile)
            if not body_versions.exists():
                get_object_or_404(BodyVersion)
            latest_body_version = body_versions.latest('created_at')
            serializer = self.serializer_class(latest_body_version)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("you don't have permission to this user data.", status=status.HTTP_406_NOT_ACCEPTABLE)




class UserBodyVersions(APIView):
    serializer_class = BodyVersionSerializer
    permission_classes = [IsCoach]

    def get(self, *args, **kwargs):
        coach = CoachProfile.objects.get(user=self.request.user)
        profile = UserProfile.objects.get(id=self.kwargs["id"])

        program = Program.objects.filter(
            Q(user=profile, coach=coach, status="completed") |
            Q(user=profile, coach=coach, status="new-and-payment-pending") |
            Q(user=profile, coach=coach, status="paid-and-waiting-for-program"))

        if program:
            version = BodyVersion.objects.filter(user=profile)
            serializer = self.serializer_class(version,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("you don't have permission to this user data.", status=status.HTTP_406_NOT_ACCEPTABLE)




class CoachProgramsMetrics(GenericAPIView):
    permission_classes = [IsCoach]
    pagination_class = CustomPagination
    serializer_class = FullProgramWithMetricSerializer
    queryset = Program.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'type', 'created_at', 'updated_at', 'coach']
    search_fields = ['status', 'type', 'description', 'target']
    ordering_fields = ['created_at', 'updated_at', 'duration_day', 'coach']

    def get(self, *args, **kwargs):
        coach = CoachProfile.objects.get(user=self.request.user)
        coach_program = Program.objects.filter(coach=coach)
        programs = self.filter_queryset(coach_program)
        page = self.paginate_queryset(programs)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.filter_queryset(coach_program)
        return Response(serializer.data, status=status.HTTP_200_OK)



class ProgramMetricItem(APIView):
    permission_classes = [IsCoach]
    serializer_class = FullProgramWithMetricSerializer
    def get(self, *args, **kwargs):
        program = Program.objects.get(id=self.kwargs["id"])
        serializer = self.serializer_class(program)
        return Response(serializer.data, status=status.HTTP_200_OK)