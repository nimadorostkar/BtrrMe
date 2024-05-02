from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.serializers import CoachProfileSerializer, UserSerializer, CertificateSerializer, GallerySerializer
from rest_framework.permissions import AllowAny
from accounts.models import User, CoachProfile, Gallery, Certificate
from accounts.views.permissions import IsCoach
from blog.models import Post
from blog.serializers import PostSerializer


class Coach(APIView):
    serializer_class = CoachProfileSerializer
    permission_classes = [IsCoach]

    def get(self, *args, **kwargs):
        coach = CoachProfile.objects.get(user=self.request.user)
        coach_serializer = self.serializer_class(coach)
        user_serializer = UserSerializer(self.request.user)
        posts = Post.objects.filter(author=coach)
        post_serializer = PostSerializer(posts, many=True)
        resp = {"user_data":user_serializer.data,"coach_data":coach_serializer.data,"coach_posts":post_serializer.data}
        return Response(resp, status=status.HTTP_200_OK)

    def patch(self, *args, **kwargs):
        coach = CoachProfile.objects.get(user=self.request.user)
        data = self.request.data
        data['user'] = coach.user.id
        serializer = self.serializer_class(coach, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    def post(self, *args, **kwargs):
        coach = CoachProfile.objects.get(user=self.request.user)
        data = self.request.data
        data['user'] = coach.user.id
        serializer = self.serializer_class(coach, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)





class CoachGallery(APIView):
    serializer_class = GallerySerializer
    permission_classes = [IsCoach]

    def get(self, *args, **kwargs):
        coach = CoachProfile.objects.get(user=self.request.user)
        gallery = Gallery.objects.filter(user=coach)
        serializer = self.serializer_class(gallery,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, *args, **kwargs):
        data = self.request.data
        data['user'] = CoachProfile.objects.get(user=self.request.user).id
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)





class CoachGalleryItem(APIView):
    serializer_class = GallerySerializer
    permission_classes = [IsCoach]

    def get(self, *args, **kwargs):
        try:
            coach = CoachProfile.objects.get(user=self.request.user)
            gallery = Gallery.objects.get(user=coach,id=self.kwargs["id"])
            serializer = self.serializer_class(gallery)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("Image not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, *args, **kwargs):
        try:
            coach = CoachProfile.objects.get(user=self.request.user)
            gallery = Gallery.objects.get(user=coach, id=self.kwargs["id"])
            gallery.delete()
            return Response("item deleted.", status=status.HTTP_200_OK)
        except:
            return Response("Something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)





class CoachCertificate(APIView):
    serializer_class = CertificateSerializer
    permission_classes = [IsCoach]

    def get(self, *args, **kwargs):
        coach = CoachProfile.objects.get(user=self.request.user)
        certificate = Certificate.objects.filter(user=coach)
        serializer = self.serializer_class(certificate,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, *args, **kwargs):
        data = self.request.data
        data['user'] = CoachProfile.objects.get(user=self.request.user).id
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)




class CoachCertificateItem(APIView):
    serializer_class = CertificateSerializer
    permission_classes = [IsCoach]

    def get(self, *args, **kwargs):
        try:
            coach = CoachProfile.objects.get(user=self.request.user)
            certificate = Certificate.objects.get(user=coach,id=self.kwargs["id"])
            serializer = self.serializer_class(certificate)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("Certificate not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, *args, **kwargs):
        try:
            coach = CoachProfile.objects.get(user=self.request.user)
            certificate = Certificate.objects.get(user=coach, id=self.kwargs["id"])
            certificate.delete()
            return Response("item deleted.", status=status.HTTP_200_OK)
        except:
            return Response("Something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)




class CoachPost(APIView):
    serializer_class = PostSerializer
    permission_classes = [IsCoach]

    def get(self, *args, **kwargs):
        coach = CoachProfile.objects.get(user=self.request.user)
        posts = Post.objects.filter(author=coach)
        serializer = self.serializer_class(posts,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, *args, **kwargs):
        data = self.request.data
        data['author'] = CoachProfile.objects.get(user=self.request.user).id
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

