from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from supplement.serializers import SupplementSerializer
from supplement.models import Supplement
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



class SupplementList(GenericAPIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination
    serializer_class = SupplementSerializer
    queryset = Supplement.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name', 'description']


    def get(self, *args, **kwargs):
        supplements = self.filter_queryset(Supplement.objects.all())
        page = self.paginate_queryset(supplements)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.filter_queryset(Supplement.objects.all())
        return Response(serializer.data, status=status.HTTP_200_OK)


class SupplementItem(APIView):
    serializer_class = SupplementSerializer
    permission_classes = [AllowAny]
    def get(self, *args, **kwargs):
        try:
            supplement = Supplement.objects.get(id=self.kwargs["id"])
            serializer = self.serializer_class(supplement)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("Supplement not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)

