from rest_framework import status
from rest_framework.response import Response
from accounts.serializers import CoachFullProfileSerializer,CoachProfileSerializer,UserSerializer,CertificateSerializer,GallerySerializer
from rest_framework.permissions import AllowAny
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from accounts.models import User, CoachProfile, Gallery, Certificate


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100



class CoachList(GenericAPIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination
    serializer_class = CoachFullProfileSerializer
    queryset = CoachProfile.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['gender']
    search_fields = ['user__first_name', 'user__last_name', 'bio']
    ordering_fields = ['id', 'gender']

    def get(self, *args, **kwargs):
        coach = self.filter_queryset(CoachProfile.objects.all())
        page = self.paginate_queryset(coach)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.filter_queryset(CoachProfile.objects.all())
        return Response(serializer.data, status=status.HTTP_200_OK)




class CoachItam(APIView):
    serializer_class = CoachProfileSerializer
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        try:
            coach = CoachProfile.objects.get(id=self.kwargs["id"])
            coach_serializer = self.serializer_class(coach)
            user_serializer = UserSerializer(coach.user)
            gallery = Gallery.objects.filter(user=coach)
            gallery_serializer = GallerySerializer(gallery, many=True)
            certificate = Certificate.objects.filter(user=coach)
            certificate_serializer = CertificateSerializer(certificate, many=True)
            resp = {"user_data": user_serializer.data, "coach_data": coach_serializer.data, "coach_gallery": gallery_serializer.data, "coach_certificate": certificate_serializer.data}
            return Response(resp, status=status.HTTP_200_OK)
        except:
            return Response("Coach not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)
