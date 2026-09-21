from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError


class ChangeContractStatusService:
    def __init__(self, actor, contract, new_status):
        self.actor = actor
        self.contract = contract
        self.new_status = new_status

    def execute(self):
        if not self.actor.has_perm(
            "contracts.activate_contract"
        ):
            raise PermissionDenied(
                "You do not have permission to change contract status."
            )

        if self.contract.status == self.new_status:
            raise ValidationError(
                "Contract already has this status."
            )

        self.contract.status = self.new_status
        self.contract.save(update_fields=["status"])

        return self.contract