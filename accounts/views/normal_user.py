from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.serializers import UserSerializer, UserProfileSerializer, BodyVersionSerializer, BodyVersionCreatSerializer
from accounts.models import User, UserProfile, BodyVersion
from accounts.views.permissions import IsNormal


class NormalUser(APIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsNormal]

    def get(self, *args, **kwargs):
        profile = UserProfile.objects.get(user=self.request.user)
        profile_serializer = self.serializer_class(profile)
        user_serializer = UserSerializer(self.request.user)
        resp = {"user_data":user_serializer.data,"profile_data":profile_serializer.data}
        return Response(resp, status=status.HTTP_200_OK)





class NormalUserBodyVersion(APIView):
    serializer_class = BodyVersionSerializer
    permission_classes = [IsNormal]
    def get(self, *args, **kwargs):
        profile = UserProfile.objects.get(user=self.request.user)
        versions = BodyVersion.objects.filter(user=profile)
        serializer = self.serializer_class(versions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, *args, **kwargs):
        profile = User.objects.get(id=self.request.user.id)
        data = self.request.data
        data['user'] = profile.id
        serializer = BodyVersionCreatSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)





class LastBodyVersion(APIView):
    serializer_class = BodyVersionSerializer
    permission_classes = [IsNormal]
    def get(self, *args, **kwargs):
        profile = UserProfile.objects.get(user=self.request.user)
        version = BodyVersion.objects.filter(user=profile).latest('created_at')
        serializer = self.serializer_class(version)
        return Response(serializer.data, status=status.HTTP_200_OK)





class UserOverview(APIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsNormal]

    def get(self, *args, **kwargs):
        profile = UserProfile.objects.get(user=self.request.user)
        profile_serializer = self.serializer_class(profile)
        user_serializer = UserSerializer(self.request.user)
        version = BodyVersion.objects.filter(user=profile).latest('created_at')
        version_serializer = BodyVersionSerializer(version)
        versions = BodyVersion.objects.filter(user=profile)
        versions_serializer = BodyVersionSerializer(versions, many=True)
        chart = []
        for vrsn in versions:
            vrsn_item = {"weight":vrsn.weight,"date":vrsn.created_at,"img":vrsn.front_double_biceps.url}
            chart.append(vrsn_item)

        resp = {"user_data": user_serializer.data,
                "profile_data": profile_serializer.data,
                "last_version": version_serializer.data,
                "versions_list": versions_serializer.data,
                "chart": chart}
        return Response(resp, status=status.HTTP_200_OK)
