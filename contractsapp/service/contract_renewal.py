from ..models import ContractModel
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
from django.utils import timezone


class RenewContractService:
    def __init__(self, actor, contract, validated_data):
        self.actor = actor
        self.contract = contract
        self.validated_data = validated_data

    def execute(self):
        if not self.actor.has_perm(
            "contracts.renew_contract"
        ):
            raise PermissionDenied(
                "You do not have permission to renew contracts."
            )

        today = timezone.localdate()

        if self.contract.end_date >= today:
            raise ValidationError(
                "Only expired contracts can be renewed."
            )

        old_values = {
            "start_date": self.contract.start_date,
            "end_date": self.contract.end_date,
            "request_quota": self.contract.request_quota,
            "rate_limit": self.contract.rate_limit,
            "status": self.contract.status,
            "used_requests": self.contract.used_requests,
        }

        for attr, value in self.validated_data.items():
            setattr(self.contract, attr, value)

        self.contract.status = ContractModel.Status.ACTIVE
        self.contract.used_requests = 0

        self.contract.full_clean()
        self.contract.save()

        return self.contract