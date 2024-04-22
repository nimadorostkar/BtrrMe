from rest_framework.permissions import IsAuthenticated


class IsCoach(IsAuthenticated):
    def has_permission(self, request, view):
        return (
            super().has_permission(request, view)
            and request.user.user_type == "coach"
        )
