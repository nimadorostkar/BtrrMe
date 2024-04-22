from rest_framework.permissions import IsAuthenticated


class IsNormal(IsAuthenticated):
    def has_permission(self, request, view):
        return (
            super().has_permission(request, view)
            and request.user.user_type == "normal"
        )
