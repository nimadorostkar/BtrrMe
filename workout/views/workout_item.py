from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from workout.serializers import WorkoutSerializer
from workout.models import Workout
from rest_framework.permissions import AllowAny



class WorkoutItem(APIView):
    serializer_class = WorkoutSerializer
    permission_classes = [AllowAny]
    def get(self, *args, **kwargs):
        try:
            workout = Workout.objects.get(id=self.kwargs["id"])
            serializer = self.serializer_class(workout)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("Workout not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)