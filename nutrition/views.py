from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from nutrition.serializers import NutritionSerializer
from nutrition.models import Nutrition
from rest_framework.permissions import AllowAny


class NutritionList(APIView):
    serializer_class = NutritionSerializer
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        serializer = self.serializer_class(Nutrition.objects.all(),many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)