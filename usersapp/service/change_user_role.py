from django.core.exceptions import PermissionDenied


class ChangeUserRoleService:

    def __init__(self, actor, target_user, new_role):
        self.actor = actor
        self.target_user = target_user
        self.new_role = new_role

    def execute(self):

        if self.actor.pk == self.target_user.pk:
            raise PermissionDenied(
                "You cannot change your own role."
            )

        current_role = self.target_user.role

        if current_role == self.target_user.Role.CLIENT:
            if self.new_role == self.target_user.Role.ADMIN:
                permission = "users.change_admin_role"

        elif current_role == self.target_user.Role.ADMIN:
            if self.new_role == self.target_user.Role.CLIENT:
                permission = "users.change_client_role"

        if not self.actor.has_perm(permission):
            raise PermissionDenied(
                "You do not have permission to change this user's role."
            )

        self.target_user.role = self.new_role
        self.target_user.save(
            update_fields=["role"]
        )

        return self.target_user