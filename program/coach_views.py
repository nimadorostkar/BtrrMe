from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from program.serializers import ProgramSerializer,FullProgramSerializer,Program_paymentSerializer
from program.models import Program,Program_payment
from rest_framework.permissions import AllowAny
from accounts.views.permissions import IsCoach, IsNormal
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import GenericAPIView
from accounts.models import CoachProfile



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


