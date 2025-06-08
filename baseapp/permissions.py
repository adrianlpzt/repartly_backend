from rest_framework.permissions import BasePermission
from baseapp.models import Profile


class IsRepartlyAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        try:
            return user.profile.is_admin_panel
        except Profile.DoesNotExist:
            return False
