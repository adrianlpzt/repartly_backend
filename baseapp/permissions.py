from rest_framework.permissions import BasePermission

class IsRepartlyAdmin(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        return user.username == getattr(user.profile, 'is_admin_panel', False)
