from .create_contract_history import CreateContractHistoryService
from django.core.exceptions import ValidationError

from rest_framework.exceptions import PermissionDenied

class ChangeContractStatusService:
    def __init__(self, actor, contract, new_status):
        self.actor = actor
        self.contract = contract
        self.new_status = new_status

    def execute(self):
        if not self.actor.has_perm(
            "contractsapp.activate_contract"
        ):
            raise PermissionDenied(
                "You do not have permission to change contract status."
            )

        if self.contract.status == self.new_status:
            raise ValidationError(
                "Contract already has this status."
            )

        old_status = self.contract.status

        self.contract.status = self.new_status
        self.contract.save(update_fields=["status"])

        CreateContractHistoryService(
            contract=self.contract,
            changed_by=self.actor,
            field_name="status",
            old_value=old_status,
            new_value=self.new_status,
        ).execute()

        return self.contract