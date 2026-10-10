import hashlib

from django.utils import timezone

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from contractsapp.models import APIKeyModel, ContractModel


class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        raw_key = request.headers.get("X-API-Key")

        if not raw_key:
            return None

        key_hash = hashlib.sha256(
            raw_key.encode("utf-8")
        ).hexdigest()

        api_key = (
            APIKeyModel.objects
            .select_related("contract", "contract__user")
            .filter(key_hash=key_hash)
            .first()
        )

        if api_key is None:
            raise AuthenticationFailed("Invalid API key.")

        if not api_key.is_active:
            raise AuthenticationFailed("API key is inactive.")

        contract = api_key.contract
        user = contract.user

        if not user.is_active:
            raise AuthenticationFailed("User is inactive.")

        if contract.status != ContractModel.Status.ACTIVE:
            raise AuthenticationFailed("Contract is inactive.")

        today = timezone.localdate()

        if not contract.start_date <= today <= contract.end_date:
            raise AuthenticationFailed("Contract is not currently valid.")

        return user, api_key

    def authenticate_header(self, request):
        return "X-API-Key"