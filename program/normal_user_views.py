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
from accounts.models import UserProfile

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserProgramsList(GenericAPIView):
    permission_classes = [IsNormal]
    pagination_class = CustomPagination
    serializer_class = FullProgramSerializer
    queryset = Program.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'type', 'created_at', 'updated_at','coach']
    search_fields = ['status', 'type', 'description', 'target']
    ordering_fields = ['created_at', 'updated_at', 'duration_day', 'coach']

    def get(self, *args, **kwargs):
        normal_user = UserProfile.objects.get(user=self.request.user)
        user_program = Program.objects.filter(user=normal_user)

        programs = self.filter_queryset(user_program)
        page = self.paginate_queryset(programs)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.filter_queryset(user_program)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserProgramsShortList(GenericAPIView):
    permission_classes = [IsNormal]
    pagination_class = CustomPagination
    serializer_class = ProgramSerializer
    queryset = Program.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'type', 'created_at', 'updated_at','coach']
    search_fields = ['status', 'type', 'description', 'target']
    ordering_fields = ['created_at', 'updated_at', 'duration_day', 'coach']

    def get(self, *args, **kwargs):
        normal_user = UserProfile.objects.get(user=self.request.user)
        user_program = Program.objects.filter(user=normal_user)

        programs = self.filter_queryset(user_program)
        page = self.paginate_queryset(programs)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.filter_queryset(user_program)
        return Response(serializer.data, status=status.HTTP_200_OK)



class UserProgramItem(APIView):
    serializer_class = FullProgramSerializer
    permission_classes = [IsNormal]
    def get(self, *args, **kwargs):
        try:
            normal_user = UserProfile.objects.get(user=self.request.user)
            user_program = Program.objects.get(user=normal_user,id=self.kwargs["id"])
            serializer = self.serializer_class(user_program)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("Program not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)



class ProgramReq(APIView):
    serializer_class = ProgramSerializer
    permission_classes = [IsNormal]
    def post(self, *args, **kwargs):
        data = self.request.data
        data['user'] = UserProfile.objects.get(user=self.request.user).id
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class ProgramPay(APIView):
    serializer_class = Program_paymentSerializer
    permission_classes = [IsNormal]
    def post(self, *args, **kwargs):
        data = self.request.data
        data['user'] = UserProfile.objects.get(user=self.request.user).id
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            program = Program.objects.get(id=self.kwargs["id"])
            program.payment = Program_payment.objects.get(id=serializer.data['id'])
            program.status = "paid-and-waiting-for-program"
            program.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)




class UserPayments(APIView):
    serializer_class = Program_paymentSerializer
    permission_classes = [IsNormal]
    def get(self, *args, **kwargs):
        try:
            user = UserProfile.objects.get(user=self.request.user)
            payments = Program_payment.objects.filter(user=user)
            serializer = self.serializer_class(payments,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("payments not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)