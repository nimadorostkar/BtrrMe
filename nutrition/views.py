from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from nutrition.serializers import NutritionSerializer
from nutrition.models import Nutrition
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



class NutritionList(GenericAPIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination
    serializer_class = NutritionSerializer
    queryset = Nutrition.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['calorie', 'fiber', 'fat', 'sugar', 'carbo', 'protein']
    search_fields = ['name', 'calorie', 'fiber', 'fat', 'sugar', 'carbo', 'protein']
    ordering_fields = ['name', 'calorie', 'fiber', 'fat', 'sugar', 'carbo', 'protein']

    def get(self, *args, **kwargs):
        nutritions = self.filter_queryset(Nutrition.objects.all())
        page = self.paginate_queryset(nutritions)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.filter_queryset(Nutrition.objects.all())
        return Response(serializer.data, status=status.HTTP_200_OK)


class NutritionItem(APIView):
    serializer_class = NutritionSerializer
    permission_classes = [AllowAny]
    def get(self, *args, **kwargs):
        try:
            nutrition = Nutrition.objects.get(id=self.kwargs["id"])
            serializer = self.serializer_class(nutrition)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("Nutrition not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)

