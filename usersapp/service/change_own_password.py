from django.contrib.auth import get_user_model
from rest_framework.exceptions import PermissionDenied

User = get_user_model()


class ChangeOwnPasswordService:
    def __init__(self, actor, new_password):
        self.actor = actor
        self.new_password = new_password

    def execute(self):
        if self.actor.role != User.Role.CLIENT:
            raise PermissionDenied(
                "Only clients can use this endpoint."
            )

        self.actor.set_password(self.new_password)
        self.actor.token_version += 1

        self.actor.save(
            update_fields=["password", "token_version"]
        )

        return self.actor