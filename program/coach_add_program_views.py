from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from program.serializers import Nutrition_programSerializer,Workout_programSerializer,Supplement_programSerializer
from program.models import Program,Program_payment, Nutrition_program, Nutrition_program_table, Workout_program,\
    Supplement_program, Supplement_program_table
from accounts.views.permissions import IsCoach
from accounts.models import User, UserProfile, BodyVersion, CoachProfile
from django.db.models import Q
from nutrition.serializers import NutritionSerializer
from nutrition.models import Nutrition
from supplement.models import Supplement



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
            program.status = "completed"
            program.save()

            return Response("Nutrion program added", status=status.HTTP_200_OK)
        else:
            return Response("you don't have permission to this user data.", status=status.HTTP_406_NOT_ACCEPTABLE)




class WorkoutProgram(APIView):
    serializer_class = Workout_programSerializer
    permission_classes = [IsCoach]
    def get(self, *args, **kwargs):
        coach = CoachProfile.objects.get(user=self.request.user)
        program = Program.objects.get(id=self.kwargs["id"])

        program_permission = Program.objects.filter(
            Q(user=program.user,coach=coach,status="completed") |
            Q(user=program.user,coach=coach,status="new-and-payment-pending") |
            Q(user=program.user, coach=coach, status="paid-and-waiting-for-program"))

        if program_permission:
            serializer = self.serializer_class(program.workout_program)
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
            serializer = self.serializer_class(data=self.request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
            program.workout_program = Workout_program.objects.get(id=serializer.data["id"])
            program.status = "completed"
            program.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("you don't have permission to this user data.", status=status.HTTP_406_NOT_ACCEPTABLE)




class SupplementProgram(APIView):
    serializer_class = Supplement_programSerializer
    permission_classes = [IsCoach]
    def get(self, *args, **kwargs):
        coach = CoachProfile.objects.get(user=self.request.user)
        program = Program.objects.get(id=self.kwargs["id"])

        program_permission = Program.objects.filter(
            Q(user=program.user,coach=coach,status="completed") |
            Q(user=program.user,coach=coach,status="new-and-payment-pending") |
            Q(user=program.user, coach=coach, status="paid-and-waiting-for-program"))

        if program_permission:
            serializer = self.serializer_class(program.supplement_program)
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
            supplement_program = Supplement_program()
            supplement_program.description = data['description']
            supplement_program.save()

            for obj in data['supplement_program_table']:
                supplement_table = Supplement_program_table()
                supplement_table.supplement_program = supplement_program
                supplement_table.supplement = Supplement.objects.get(id=obj['supplement'])
                supplement_table.qty = obj['qty']
                supplement_table.time = obj['time']
                supplement_table.save()

            program.supplement_program = supplement_program
            program.status = "completed"
            program.save()

            return Response("Supplement program added", status=status.HTTP_200_OK)
        else:
            return Response("you don't have permission to this user data.", status=status.HTTP_406_NOT_ACCEPTABLE)
