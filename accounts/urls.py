from django.urls import path
from accounts.views import Logout,Profile,Refresh,RefreshAccess,SendOTP,VerifyOTP,\
    CompleteRegistration,Coach,CoachGallery,CoachGalleryItem,CoachCertificate,\
    CoachCertificateItem,CoachList,CoachItam,CoachPost,NormalUser,UserOverview,\
    NormalUserBodyVersion,LastBodyVersion,CoachPostItem,CoachPostCats,CoachWorkExperience,\
    WorkExperienceItem,CoachAthletes


urlpatterns = [
    path("otp", SendOTP.as_view(), name="send_otp"),
    path("otp/verify", VerifyOTP.as_view(), name="verify_otp"),
    path("complete-registration", CompleteRegistration.as_view(), name="complete-registration"),
    path("refresh", Refresh.as_view(), name="refresh"),
    path("refresh-access", RefreshAccess.as_view(), name="refresh-access"),
    path("logout", Logout.as_view(), name="logout"),
    path("profile", Profile.as_view(), name="profile"),
    # coach
    path("coach", Coach.as_view(), name="coach"),
    path("coach-athletes", CoachAthletes.as_view(), name="coach-athletes"),
    path("coach-gallery", CoachGallery.as_view(), name="coach-gallery"),
    path("coach-gallery-item/<int:id>", CoachGalleryItem.as_view(), name="coach-gallery-item"),
    path("coach-certificate", CoachCertificate.as_view(), name="coach-certificate"),
    path("coach-certificate-item/<int:id>", CoachCertificateItem.as_view(), name="coach-certificate-item"),
    path("coach-list", CoachList.as_view(), name="coach-list"),
    path("coach-item/<int:id>", CoachItam.as_view(), name="coach-item"),
    path("coach-post", CoachPost.as_view(), name="coach-post"),
    path('coach-post-item/<int:id>', CoachPostItem.as_view(), name='coach-post-item'),
    path("coach-post-cats", CoachPostCats.as_view(), name="coach-post-cats"),
    path("work-exp", CoachWorkExperience.as_view(), name="work-exp"),
    path('work-exp-item/<int:id>', WorkExperienceItem.as_view(), name='work-exp-item'),
    # normal user
    path("normal", NormalUser.as_view(), name="normal"),
    path("normal-overview", UserOverview.as_view(), name="normal-overview"),
    path("body-version", NormalUserBodyVersion.as_view(), name="body-version"),
    path("last-body-version", LastBodyVersion.as_view(), name="last-body-version"),
]
