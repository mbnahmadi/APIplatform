from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    message = "Only admins can access to this api."
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated and request.user.role == "admin")        

class CanViewUsers(BasePermission):
    message = "only admins whith view users permission can access to this api."
    def has_permission(self, request, view):
        return request.user.has_perm("usersapp.view_user")


class CanManagePermissions(BasePermission):

    def has_permission(self, request, view):
        return request.user.has_perm(
            "usersapp.manage_permissions"
        )