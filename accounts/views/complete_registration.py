from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.serializers import UserSerializer,UserProfileSerializer,CoachProfileSerializer
from accounts.models import User,CoachProfile,UserProfile,BodyVersion


class CompleteRegistration(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, *args, **kwargs):
        user = self.request.user
        data = self.request.data
        data['phone_number'] = user.phone_number

        serializer = UserSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            if data['user_type'] == "coach":
                if CoachProfile.objects.filter(user=user).exists():
                    coach = CoachProfile.objects.get(user=user)
                else:
                    coach = CoachProfile()
                coach.user = user
                coach.save()
                profile_serializer = CoachProfileSerializer(coach)
            elif data['user_type'] == "normal":
                if UserProfile.objects.filter(user=user).exists():
                    normal = UserProfile.objects.get(user=user)
                else:
                    normal = UserProfile()
                normal.user = user
                normal.save()
                metric = BodyVersion()
                metric.user = normal
                metric.save()
                profile_serializer = UserProfileSerializer(normal)
            else:
                return Response("Error in complete registration", status=status.HTTP_406_NOT_ACCEPTABLE)

            reponse_data={"user_data":serializer.data,"profile_data":profile_serializer.data}
            return Response(reponse_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
