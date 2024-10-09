from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.serializers import UserSerializer, UserProfileSerializer, BodyVersionSerializer, BodyVersionCreatSerializer
from accounts.models import User, UserProfile, BodyVersion
from accounts.views.permissions import IsNormal
from django.shortcuts import get_object_or_404


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
        #profile = User.objects.get(id=self.request.user.id)
        profile = UserProfile.objects.get(user=self.request.user)
        data = self.request.data.copy()
        data['user'] = profile.id
        serializer = BodyVersionCreatSerializer(data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)





class LastBodyVersion(APIView):
    serializer_class = BodyVersionSerializer
    permission_classes = [IsNormal]
    def get(self, *args, **kwargs):
        profile = UserProfile.objects.get(user=self.request.user)
        version = BodyVersion.objects.filter(user=profile)
        if not version.exists():
            get_object_or_404(BodyVersion)
        latest_body_version = version.last()
        serializer = self.serializer_class(latest_body_version)
        return Response(serializer.data, status=status.HTTP_200_OK)





class UserOverview(APIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsNormal]

    def get(self, *args, **kwargs):
        profile = UserProfile.objects.get(user=self.request.user)
        profile_serializer = self.serializer_class(profile)
        user_serializer = UserSerializer(self.request.user)

        version = BodyVersion.objects.filter(user=profile)

        if not version.exists():
            last_version = []
        else:
            latest_body_version = version.last()
            last_version = BodyVersionSerializer(latest_body_version).data



        chart = []
        for vrsn in version:
            vrsn_item = {"weight":vrsn.weight,"date":vrsn.created_at,"img":vrsn.front_double_biceps.url}
            chart.append(vrsn_item)

        resp = {"user_data": user_serializer.data,
                "profile_data": profile_serializer.data,
                "last_version": last_version,
                "versions_list": BodyVersionSerializer(version, many=True).data,
                "chart": chart}
        return Response(resp, status=status.HTTP_200_OK)
