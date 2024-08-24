from django.urls import path
from contact.views import AddContact

urlpatterns = [
    path("add", AddContact.as_view(), name="add"),
]