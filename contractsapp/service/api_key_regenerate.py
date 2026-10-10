import hashlib
import secrets

from django.db import transaction
from django.utils import timezone
from django.contrib.auth import get_user_model

from rest_framework.exceptions import ValidationError, PermissionDenied

from ..models import APIKeyModel, ContractModel

User = get_user_model()


class RegenerateAPIKeyService:
    def __init__(self, actor, contract):
        self.actor = actor
        self.contract = contract

    @transaction.atomic
    def execute(self):
        if self.actor.role != User.Role.CLIENT:
            raise PermissionDenied(
                "Only clients can regenerate API keys."
            )

        if self.contract.user_id != self.actor.id:
            raise PermissionDenied(
                "You cannot regenerate an API key for this contract."
            )

        if not self.actor.is_active:
            raise PermissionDenied(
                "Inactive users cannot regenerate API keys."
            )

        if self.contract.status != ContractModel.Status.ACTIVE:
            raise ValidationError(
                "Cannot regenerate API key for an inactive contract."
            )

        today = timezone.localdate()

        if not (
            self.contract.start_date
            <= today
            <= self.contract.end_date
        ):
            raise ValidationError(
                "Contract is not currently valid."
            )

        old_key = (
            APIKeyModel.objects
            .select_for_update()
            .filter(
                contract=self.contract,
                is_active=True,
            )
            .first()
        )

        if old_key is None:
            raise ValidationError(
                "No active API key exists. Generate one first."
            )

        old_key.is_active = False
        old_key.deactivated_at = timezone.now()
        old_key.save(
            update_fields=["is_active", "deactivated_at"]
        )

        raw_key = secrets.token_urlsafe(32)

        key_hash = hashlib.sha256(
            raw_key.encode("utf-8")
        ).hexdigest()

        APIKeyModel.objects.create(
            contract=self.contract,
            key_hash=key_hash,
        )

        return raw_key