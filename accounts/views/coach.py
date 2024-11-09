from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.serializers import CoachProfileSerializer, UserSerializer, CertificateSerializer, \
    GallerySerializer, WorkExperienceSerializer, UserUpdateSerializer
from rest_framework.permissions import AllowAny
from accounts.models import User, CoachProfile, Gallery, Certificate, WorkExperience, UserProfile
from accounts.views.permissions import IsCoach
from blog.models import Post, Category
from blog.serializers import PostSerializer, CategorySerializer, PostEditSerializer, PostDetailSerializer
from program.models import Program
from datetime import datetime, timedelta




class CoachFull(APIView):
    serializer_class = CoachProfileSerializer
    permission_classes = [IsCoach]
    def get(self, *args, **kwargs):
        coach = CoachProfile.objects.get(user=self.request.user)
        coach_serializer = self.serializer_class(coach)
        user_serializer = UserSerializer(self.request.user)
        posts = Post.objects.filter(author=coach)
        post_serializer = PostSerializer(posts, many=True)

        program_users = Program.objects.filter(coach=coach).values_list('user', flat=True).distinct()
        user_program_userid = []
        for user in program_users:
            user_program_userid.append(user)
        athletes = []
        for userid in user_program_userid:
            program = Program.objects.filter(coach=coach, user=userid).latest('created_at')
            end_date = program.created_at + timedelta(days=program.duration_day)
            remaining_days = (end_date - datetime.now().date()).days
            athlete = {'base_user_id': program.user.user.id,
                       'user_profile_id': program.user.id,
                       'first_name': program.user.user.first_name,
                       'last_name': program.user.user.last_name,
                       'phone_number': program.user.user.phone_number,
                       'user_image': program.user.image.url,
                       'program_type': program.type,
                       'program_status': program.status,
                       'remaining_days': remaining_days}
            athletes.append(athlete)

        certificate = Certificate.objects.filter(user=coach)
        cert_serializer = self.serializer_class(certificate, many=True)

        gallery = Gallery.objects.filter(user=coach)
        gallery_serializer = self.serializer_class(gallery, many=True)

        resp = {"user_data":user_serializer.data,
                "coach_data":coach_serializer.data,
                "coach_posts":post_serializer.data,
                "coach_athletes":athletes,
                "coach_certificates": cert_serializer.data,
                "coach_gallery": gallery_serializer.data
                }
        return Response(resp, status=status.HTTP_200_OK)

    def patch(self, *args, **kwargs):
        user = self.request.user
        data = self.request.data
        user_serializer = UserUpdateSerializer(user, data=data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
        coach = CoachProfile.objects.get(user=self.request.user)
        serializer = self.serializer_class(coach, data=data, partial=True)
        data['user'] = coach.user.id
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    def post(self, *args, **kwargs):
        coach = CoachProfile.objects.get(user=self.request.user)
        serializer = self.serializer_class(coach, data=self.request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)




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
        serializer = PostDetailSerializer(posts,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, *args, **kwargs):
        data = self.request.data
        data2 = data.copy()
        data2['author'] = CoachProfile.objects.get(user=self.request.user).id
        serializer = self.serializer_class(data=data2,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class CoachPostCats(APIView):
    serializer_class = CategorySerializer
    permission_classes = [IsCoach]

    def get(self, *args, **kwargs):
        cats = Category.objects.all()
        serializer = self.serializer_class(cats,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class CoachPostItem(APIView):
    serializer_class = PostSerializer
    permission_classes = [IsCoach]

    def get(self, *args, **kwargs):
        try:
            coach = CoachProfile.objects.get(user=self.request.user)
            post = Post.objects.get(id=self.kwargs["id"],author=coach)
            serializer = self.serializer_class(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("Post not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)

    def patch(self, *args, **kwargs):
        coach = CoachProfile.objects.get(user=self.request.user)
        post = Post.objects.get(id=self.kwargs["id"], author=coach)
        #data['author'] = coach.id
        serializer = PostEditSerializer(post, data=self.request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, *args, **kwargs):
        try:
            coach = CoachProfile.objects.get(user=self.request.user)
            post = Post.objects.get(id=self.kwargs["id"], author=coach)
            post.delete()
            return Response("Invoice deleted", status=status.HTTP_200_OK)
        except:
            return Response("Something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)





class CoachWorkExperience(APIView):
    serializer_class = WorkExperienceSerializer
    permission_classes = [IsCoach]

    def get(self, *args, **kwargs):
        coach = CoachProfile.objects.get(user=self.request.user)
        work_exp = WorkExperience.objects.filter(user=coach)
        serializer = self.serializer_class(work_exp,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, *args, **kwargs):
        data = self.request.data
        data['user'] = CoachProfile.objects.get(user=self.request.user).id
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)




class WorkExperienceItem(APIView):
    serializer_class = WorkExperienceSerializer
    permission_classes = [IsCoach]

    def get(self, *args, **kwargs):
        try:
            coach = CoachProfile.objects.get(user=self.request.user)
            work_exp = WorkExperience.objects.get(id=self.kwargs["id"],user=coach)
            serializer = self.serializer_class(work_exp)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("Work Experience not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)

    def patch(self, *args, **kwargs):
        coach = CoachProfile.objects.get(user=self.request.user)
        work_exp = WorkExperience.objects.get(id=self.kwargs["id"],user=coach)
        serializer = WorkExperienceSerializer(work_exp, data=self.request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, *args, **kwargs):
        try:
            coach = CoachProfile.objects.get(user=self.request.user)
            work_exp = WorkExperience.objects.get(id=self.kwargs["id"],user=coach)
            work_exp.delete()
            return Response("Work Experience deleted", status=status.HTTP_200_OK)
        except:
            return Response("Something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)




class CoachAthletes(APIView):
    serializer_class = CoachProfileSerializer
    permission_classes = [IsCoach]

    def get(self, *args, **kwargs):
        coach = CoachProfile.objects.get(user=self.request.user)
        program_users = Program.objects.filter(coach=coach).values_list('user', flat=True).distinct()

        user_program_userid = []
        for user in program_users:
            user_program_userid.append(user)

        athletes = []
        for userid in user_program_userid:
            program = Program.objects.filter(coach=coach,user=userid).latest('created_at')
            end_date = program.created_at + timedelta(days=program.duration_day)
            remaining_days = (end_date - datetime.now().date()).days
            athlete = {'base_user_id': program.user.user.id,
                       'user_profile_id': program.user.id,
                       'first_name': program.user.user.first_name,
                       'last_name': program.user.user.last_name,
                       'phone_number': program.user.user.phone_number,
                       'user_image': program.user.image.url,
                       'program_type': program.type,
                       'program_status': program.status,
                       'remaining_days': remaining_days}
            athletes.append(athlete)

        return Response(athletes, status=status.HTTP_200_OK)


class CoachCounts(APIView):
    serializer_class = CoachProfileSerializer
    permission_classes = [IsCoach]
    def get(self, *args, **kwargs):
        coach = CoachProfile.objects.get(user=self.request.user)

        programs = Program.objects.filter(coach=coach)
        program_users = programs.values_list('user', flat=True).distinct()
        posts = Post.objects.filter(author=coach)

        data = {"athletes_count":program_users.count(), "posts_count":posts.count(), "programs_count":programs.count()}
        return Response(data, status=status.HTTP_200_OK)
