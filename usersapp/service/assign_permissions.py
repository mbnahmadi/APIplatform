
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Permission


class AssignPermissionService:

    def __init__(self, actor, target_user, permission):
        self.actor = actor
        self.target_user = target_user
        self.permission = permission

    def execute(self):

        # Actor must have permission-management access
        if not self.actor.has_perm("usersapp.manage_permissions"):
            raise PermissionDenied(
                "You do not have permission to manage permissions."
            )

        # Target must be an Admin
        if self.target_user.role != self.target_user.Role.ADMIN:
            raise PermissionDenied(
                "Permissions can only be assigned to admins."
            )

        # Admin cannot assign permissions to himself
        if self.actor.pk == self.target_user.pk:
            raise PermissionDenied(
                "You cannot assign permissions to yourself."
            )

        # manage_permissions cannot be assigned through this API
        if (
            self.permission.content_type.app_label == "usersapp"
            and self.permission.codename == "manage_permissions"
        ):
            raise PermissionDenied(
                "This permission cannot be assigned."
            )

        # Do not create a duplicate relation
        if self.target_user.user_permissions.filter(
            pk=self.permission.pk
        ).exists():
            raise ValueError(
                "This user already has this permission."
            )

        self.target_user.user_permissions.add(self.permission)

        return self.permission