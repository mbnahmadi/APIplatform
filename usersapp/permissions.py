from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    message = "Only admins can access to this api."
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated and request.user.role == "admin")        