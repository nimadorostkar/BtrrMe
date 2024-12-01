from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.serializers import UserSerializer, UserProfileSerializer, BodyVersionSerializer, \
    BodyVersionCreatSerializer, UserUpdateSerializer
from accounts.models import User, UserProfile, BodyVersion
from accounts.views.permissions import IsNormal
from django.shortcuts import get_object_or_404
from program.models import Program
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.http import HttpResponse,JsonResponse
from datetime import datetime


class NormalFull(APIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsNormal]
    def get(self, *args, **kwargs):
        normal_profile = UserProfile.objects.get(user=self.request.user)
        normal_serializer = self.serializer_class(normal_profile)
        user_serializer = UserSerializer(self.request.user)
        version = BodyVersion.objects.filter(user=normal_profile).order_by('-created_at')

        if not version.exists():
            last_version = []
        else:
            latest_body_version = version.latest('created_at')
            last_version = BodyVersionSerializer(latest_body_version).data

        chart = []
        for vrsn in version:
            vrsn_item = {"weight": vrsn.weight, "date": vrsn.created_at, "img": vrsn.front_double_biceps.url}
            chart.append(vrsn_item)

        resp = {"user_data":user_serializer.data,
                "profile_data":normal_serializer.data,
                "last_version": last_version,
                "versions_list": BodyVersionSerializer(version, many=True).data,
                "chart": chart}
        return Response(resp, status=status.HTTP_200_OK)

    def patch(self, *args, **kwargs):
        user = self.request.user
        data = self.request.data
        user_serializer = UserUpdateSerializer(user, data=data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
        normal_profile = UserProfile.objects.get(user=self.request.user)
        serializer = self.serializer_class(normal_profile, data=data, partial=True)
        data['user'] = normal_profile.user.id
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    def post(self, *args, **kwargs):
        normal_profile = UserProfile.objects.get(user=self.request.user)
        serializer = self.serializer_class(normal_profile, data=self.request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)







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
        versions = BodyVersion.objects.filter(user=profile).order_by('-created_at')
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
        latest_body_version = version.latest('created_at')
        serializer = self.serializer_class(latest_body_version)
        return Response(serializer.data, status=status.HTTP_200_OK)





class UserOverview(APIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsNormal]

    def get(self, *args, **kwargs):
        profile = UserProfile.objects.get(user=self.request.user)
        profile_serializer = self.serializer_class(profile)
        user_serializer = UserSerializer(self.request.user)

        version = BodyVersion.objects.filter(user=profile).order_by('-created_at')

        if not version.exists():
            last_version = []
        else:
            latest_body_version = version.latest('created_at')
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




class VersionItem(APIView):
    serializer_class = BodyVersionSerializer
    permission_classes = [IsNormal]

    def get(self, *args, **kwargs):
        try:
            profile = UserProfile.objects.get(user=self.request.user)
            version = BodyVersion.objects.get(id=self.kwargs["id"],user=profile)
            serializer = self.serializer_class(version)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("Version not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)

    def patch(self, *args, **kwargs):
        profile = UserProfile.objects.get(user=self.request.user)
        version = BodyVersion.objects.get(id=self.kwargs["id"], user=profile)
        serializer = self.serializer_class(version, data=self.request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, *args, **kwargs):
        try:
            profile = UserProfile.objects.get(user=self.request.user)
            version = BodyVersion.objects.get(id=self.kwargs["id"], user=profile)
            version.delete()
            return Response("Version deleted", status=status.HTTP_200_OK)
        except:
            return Response("Something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)





class Updates(APIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsNormal]

    def get(self, *args, **kwargs):
        try:
            profile = UserProfile.objects.get(user=self.request.user)
            update_list = []

            version = BodyVersion.objects.filter(user=profile)
            for Ver in version:
                natural_date = naturaltime(Ver.created_at)
                metric = f"متریک بدنی جدید در {natural_date} اضافه شد"
                update_list.append(metric)
                activity = f"سطح فعالیت به روز شد به {Ver.activity_type}"
                update_list.append(activity)

            program = Program.objects.filter(user=profile, status="paid-and-waiting-for-program")
            for Pro in program:
                natural_date = naturaltime(Pro.created_at)
                new_program = f"درخواست برنامه جدید در {natural_date}"
                update_list.append(new_program)

            complete_program = Program.objects.filter(user=profile, status="completed")
            for ComPro in complete_program:
                converted_datetime = datetime.combine(ComPro.program_receive_at, datetime.min.time())
                natural_date = naturaltime(converted_datetime)
                com_program = f"برنامه شما تکمیل شد در {natural_date}"
                update_list.append(com_program)

            return Response(update_list, status=status.HTTP_200_OK)


        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)