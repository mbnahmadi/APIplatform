from django.db import transaction
from django.utils import timezone

from rest_framework.exceptions import ValidationError, PermissionDenied

from ..models import APIKeyModel


class RevokeAPIKeyService:
    def __init__(self, actor, api_key):
        self.actor = actor
        self.api_key = api_key

    @transaction.atomic
    def execute(self):
        if not self.actor.has_perm(
            "contractsapp.revoke_api_key"
        ):
            raise PermissionDenied(
                "You do not have permission to revoke API keys."
            )

        api_key = (
            APIKeyModel.objects
            .select_for_update()
            .get(pk=self.api_key.pk)
        )

        if not api_key.is_active:
            raise ValidationError(
                "This API key is already inactive."
            )

        api_key.is_active = False
        api_key.deactivated_at = timezone.now()

        api_key.save(
            update_fields=["is_active", "deactivated_at"]
        )

        return api_key