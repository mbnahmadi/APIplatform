from ..models import ContractModel
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import transaction


from .create_contract_history import CreateContractHistoryService


class RenewContractService:
    def __init__(self, actor, contract, validated_data):
        self.actor = actor
        self.contract = contract
        self.validated_data = validated_data

    @transaction.atomic
    def execute(self):
        if not self.actor.has_perm(
            "contractsapp.renew_contract"
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

        for field, value in self.validated_data.items():
            setattr(self.contract, field, value)

        self.contract.status = ContractModel.Status.ACTIVE
        self.contract.used_requests = 0

        self.contract.full_clean()
        self.contract.save()

        for field, old_value in old_values.items():
            new_value = getattr(
                self.contract,
                field,
            )

            if old_value != new_value:
                CreateContractHistoryService(
                    contract=self.contract,
                    changed_by=self.actor,
                    field_name=field,
                    old_value=old_value,
                    new_value=new_value,
                ).execute()

        return self.contract