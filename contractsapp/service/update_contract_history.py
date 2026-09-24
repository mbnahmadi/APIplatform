from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
from django.utils import timezone

from ..models import ContractModel
from .create_contract_history import CreateContractHistoryService


class UpdateContractService:
    def __init__(self, actor, contract, validated_data):
        self.actor = actor
        self.contract = contract
        self.validated_data = validated_data

    def execute(self):
        if not self.actor.has_perm(
            "contracts.update_contract"
        ):
            raise PermissionDenied(
                "You do not have permission to update contracts."
            )

        today = timezone.localdate()

        if self.contract.status != ContractModel.Status.ACTIVE:
            raise ValidationError(
                "Only active contracts can be updated."
            )

        if self.contract.end_date < today:
            raise ValidationError(
                "Expired contracts cannot be updated."
            )

        old_values = {
            field: getattr(self.contract, field)
            for field in self.validated_data
        }

        for attr, value in self.validated_data.items():
            setattr(self.contract, attr, value)

        self.contract.full_clean()
        self.contract.save()

        for field, new_value in self.validated_data.items():
            old_value = old_values[field]

            if old_value != new_value:
                CreateContractHistoryService(
                    contract=self.contract,
                    changed_by=self.actor,
                    field_name=field,
                    old_value=old_value,
                    new_value=new_value,
                ).execute()

        return self.contract