from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from workout.serializers import WorkoutSerializer
from workout.models import Workout
from rest_framework.permissions import AllowAny
from accounts.views.permissions import IsCoach, IsNormal
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import GenericAPIView


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100



class WorkoutList(GenericAPIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination
    serializer_class = WorkoutSerializer
    queryset = Workout.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['place', 'muscle', 'muscle__english_name', 'type', 'equipment', 'equipment__name', 'gender', 'hardness']
    search_fields = ['name', 'english_name', 'description']
    ordering_fields = ['place', 'muscle', 'type', 'gender']

    def get(self, *args, **kwargs):
        workouts = self.filter_queryset(Workout.objects.all())
        page = self.paginate_queryset(workouts)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.filter_queryset(Workout.objects.all())
        return Response(serializer.data, status=status.HTTP_200_OK)

