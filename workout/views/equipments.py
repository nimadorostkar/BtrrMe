from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from workout.serializers import EquipmentSerializer
from workout.models import Equipment
from rest_framework.permissions import AllowAny


class Equipments(APIView):
    serializer_class = EquipmentSerializer
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        equipment = Equipment.objects.all()
        serializer = self.serializer_class(equipment, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)