from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied

User = get_user_model()


class AdminChangeClientPasswordService:
    def __init__(self, actor, user_id, new_password):
        self.actor = actor
        self.user_id = user_id
        self.new_password = new_password

    def execute(self):
        if not self.actor.has_perm("usersapp.change_client_password"):
            raise PermissionDenied(
                "You do not have permission to change client passwords."
            )

        target_user = get_object_or_404(
            User,
            pk=self.user_id,
        )

        if target_user.role != User.Role.CLIENT:
            raise PermissionDenied(
                "You can only change client passwords."
            )

        target_user.set_password(self.new_password)
        target_user.token_version += 1

        target_user.save(
            update_fields=["password", "token_version"]
        )

        return target_user