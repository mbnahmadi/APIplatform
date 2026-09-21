from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
from django.utils import timezone

from ..models import ContractModel


class UpdateContractService:
    def __init__(self, actor, contract, validated_data):
        self.actor = actor
        self.contract = contract
        self.validated_data = validated_data

    def execute(self):
        if not self.actor.has_perm(
            "contractsapp.update_contract"
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

        for attr, value in self.validated_data.items():
            setattr(self.contract, attr, value)


        self.contract.full_clean()
        self.contract.save()

        return self.contract