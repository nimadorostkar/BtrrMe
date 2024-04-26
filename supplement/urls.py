from django.urls import path
from supplement.views import SupplementList, SupplementItem

urlpatterns = [
    path("list", SupplementList.as_view(), name="list"),
    path('supplement-item/<int:id>', SupplementItem.as_view(), name='supplement-item'),
]