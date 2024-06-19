from django.urls import path
from program.normal_user_views import UserProgramsList,UserProgramsShortList,UserProgramItem,ProgramReq,ProgramPay,UserPayments
from program.coach_views import CoachProgramsList,CoachProgramsShortList, UserLastBodyVersion,UserBodyVersions, CoachProgramsMetrics


urlpatterns = [
    path("user-programs", UserProgramsList.as_view(), name="user-programs"),
    path("user-programs-short-data", UserProgramsShortList.as_view(), name="user-programs-short-data"),
    path('user-program-item/<int:id>', UserProgramItem.as_view(), name='user-program-item'),
    path("program-req", ProgramReq.as_view(), name="program-req"),
    path('program-pay/<int:id>', ProgramPay.as_view(), name='program-pay'),
    path('user-payments', UserPayments.as_view(), name='user-payments'),
    #
    path("coach-programs", CoachProgramsList.as_view(), name="coach-programs"),
    path("programs-metrics", CoachProgramsMetrics.as_view(), name="programs-metrics"),
    path("coach-programs-short-data", CoachProgramsShortList.as_view(), name="coach-programs-short-data"),
    path('user-last-body-version/<int:id>', UserLastBodyVersion.as_view(), name='user-last-body-version'),
    path('user-body-versions/<int:id>', UserBodyVersions.as_view(), name='user-body-versions'),
]


