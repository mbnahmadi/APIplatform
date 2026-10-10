import hashlib
import secrets

# from django.core.exceptions import ValidationError
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth import get_user_model

from ..models import APIKeyModel, ContractModel
# from users.models import User


User = get_user_model()

class GenerateAPIKeyService:
    def __init__(self, actor, contract):
        self.actor = actor
        self.contract = contract

    def execute(self):
        if self.actor.role != User.Role.CLIENT:
            raise ValidationError(
                "Only clients can generate API keys."
            )

        if self.contract.user_id != self.actor.id:
            raise ValidationError(
                "You cannot generate an API key for this contract."
            )

        if not self.actor.is_active:
            raise ValidationError(
                "Inactive users cannot generate API keys."
            )

        if self.contract.status != ContractModel.Status.ACTIVE:
            raise ValidationError(
                "Cannot generate API key for an inactive contract."
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

        existing_key = APIKeyModel.objects.filter(
            contract=self.contract,
            is_active=True,
        ).exists()

        if existing_key:
            raise ValidationError(
                "This contract already has an active API key."
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