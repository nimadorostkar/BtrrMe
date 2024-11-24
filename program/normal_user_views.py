from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from program.serializers import ProgramSerializer,FullProgramSerializer,TransactionSerializer
from program.models import Program,Transaction
from rest_framework.permissions import AllowAny
from accounts.views.permissions import IsCoach, IsNormal
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import GenericAPIView
from accounts.models import UserProfile
from datetime import datetime
from openai import OpenAI
from django.utils import timezone
import json
import requests
from django.conf import settings
from django.db import transaction
from config.responses import bad_request, SuccessResponse, UnsuccessfulResponse
from django.http import HttpResponse,JsonResponse
from django.shortcuts import redirect
from decimal import Decimal


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





class ProgramReqAI(APIView):
    serializer_class = ProgramSerializer
    permission_classes = [AllowAny]
    def post(self, *args, **kwargs):
        prompt = """
        You are a fitness coach and expert in designing effective workout programs. 
        Create a structured 5-day fitness workout program tailored for an intermediate individual with the following details:

        - User Information:
          - Profession: Professional bodybuilder with 7 years of training experience.
          - Goal: Increase muscle mass and burn fat.
          - Training Frequency: 5 days per week.

        - Equipment Available:
          - Barbell, benches, dumbbells, cables, treadmill.

        - Requirements:
          - Include at least 10 exercises for each training day.
          - Specify the number of sets and reps for each exercise.
          - Focus on progressive overload and balanced muscle group targeting.
          - Integrate cardio for fat-burning where necessary.

        - Output:
          - Return the plan in a clean JSON format, structured as follows:
            {
              "Saturday": {
                "muscle_name":"Chest day",
                "Exercises": [
                  {
                    "Name": "Exercise Name",
                    "Sets": Number,
                    "Reps": Number
                  },
                  ...
                ]
              },
              ...
            }
        """

        assistant = "As a sports assistant, you can provide him with a sports program based on the user's information"

        try:
            client = OpenAI(
                api_key="ttttt")
            response = client.chat.completions.create(
                model="gpt-4",  # Replace with your desired model gpt-4o-mini
                messages=[
                    {"role": "user", "content": prompt},
                    {"role": "system", "content": assistant},
                ],
                max_tokens=2000,  # Adjust as needed
                stop=None,
                temperature=0.7)
            # final_response = response.choices[0].message['content']
            response_dict = response.model_dump()
            message_content = response_dict['choices'][0]['message']['content']
            print('---------------')
            print(message_content)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(message_content, status=status.HTTP_200_OK)








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
    serializer_class = TransactionSerializer
    permission_classes = [IsNormal]
    def get(self, *args, **kwargs):
        authority = self.request.query_params.get("Authority")
        status = self.request.query_params.get("Status")

        try:
            program = Program.objects.get(id=self.kwargs["id"])
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        print('-----')
        print(program.price())

        data = {
            "MerchantID": settings.ZARRINPAL_MERCHANT_ID,
            "Amount": program.price(),
            "Description": "هزینه دریافت برنامه آنلاین از بترمی",
            "Authority": authority,
            "Phone": program.user.user.phone_number,
            "CallbackURL": settings.ZARIN_CALL_BACK + str(program.id) + "/",
            "OrderID": program.id,
            "wages": [{
                "iban": "33333333333",
                "amount": Decimal(program.price())*Decimal("0.15"),
                "description": "تسهیم سود فروش از برنامه"
              }],
            }
        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}

        try:
            response = requests.post(settings.ZP_API_REQUEST, data=data, headers=headers, timeout=10)
            response.raise_for_status()

            if response.status_code == 200:
                response = response.json()
                print('---------------')
                print(response)
                if response['Status'] == 100:
                    transaction = Transaction(user=program.user,price=program.price(),paid=True,authority=response['Authority'])
                    transaction.save()
                    program.payment = transaction
                    program.status = "paid-and-waiting-for-program"
                    program.save()
                    transaction_serializer = TransactionSerializer(transaction)
                    data = {'status': True, 'url': settings.ZP_API_STARTPAY + str(response['Authority']),
                            'order': program.id, 'authority': response['Authority']}
                    return SuccessResponse(transaction_serializer.data, data)
                else:
                    return Response(response['errors'], status=400)
            return response

        except requests.exceptions.Timeout:
            return {'status': False, 'code': 'timeout'}
        except requests.exceptions.ConnectionError:
            return {'status': False, 'code': 'connection error'}





class UserPayments(APIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsNormal]
    def get(self, *args, **kwargs):
        try:
            user = UserProfile.objects.get(user=self.request.user)
            payments = Transaction.objects.filter(user=user)
            serializer = self.serializer_class(payments,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("payments not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)