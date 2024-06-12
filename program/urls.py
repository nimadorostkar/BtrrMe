from django.urls import path
from program.views import UserProgramsList,UserProgramsShortList,UserProgramItem

urlpatterns = [
    path("user-programs", UserProgramsList.as_view(), name="user-programs"),
    path("user-programs-short-data", UserProgramsShortList.as_view(), name="user-programs-short-data"),
    path('user-program-item/<int:id>', UserProgramItem.as_view(), name='user-program-item'),
]


program-req