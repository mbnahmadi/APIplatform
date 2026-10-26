from django.db import transaction
from rest_framework.exceptions import PermissionDenied, NotFound

from usersapp.models import User


class UpdateUserProfileService:
    def __init__(self, actor, user_id, validated_data):
        self.actor = actor
        self.user_id = user_id
        self.validated_data = validated_data

    @transaction.atomic
    def execute(self):
        if not self.actor.has_perm("usersapp.change_user_profile"):
            raise PermissionDenied(
                "You do not have permission to change user profiles."
            )

        user = (
            User.objects.select_for_update()
            .filter(pk=self.user_id)
            .first()
        )

        if user is None:
            raise NotFound("User not found.")

        for field, value in self.validated_data.items():
            setattr(user, field, value)

        if self.validated_data:
            user.save(update_fields=list(self.validated_data.keys()))

        return user