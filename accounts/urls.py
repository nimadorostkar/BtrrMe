from django.urls import path
from accounts.views import Logout,Profile,Refresh,RefreshAccess,SendOTP,VerifyOTP,CompleteRegistration


urlpatterns = [
    path("otp", SendOTP.as_view(), name="send_otp"),
    path("otp/verify", VerifyOTP.as_view(), name="verify_otp"),
    path("complete-registration", CompleteRegistration.as_view(), name="complete-registration"),
    path("refresh", Refresh.as_view(), name="refresh"),
    path("refresh-access", RefreshAccess.as_view(), name="refresh-access"),
    path("logout", Logout.as_view(), name="logout"),
    path("profile", Profile.as_view(), name="profile"),
]
