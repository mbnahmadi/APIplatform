from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import NotFound, PermissionDenied

from ..models import ContractParameterModel


class RevokeParameterAssignmentService:
    def __init__(self, actor, contract_id, parameter_id):
        self.actor = actor
        self.contract_id = contract_id
        self.parameter_id = parameter_id

    @transaction.atomic
    def execute(self):
        if not self.actor.has_perm("contractsapp.remove_parameter"):
            raise PermissionDenied(
                "You do not have permission to revoke parameter assignments."
            )

        assignment = (
            ContractParameterModel.objects
            .select_for_update()
            .filter(
                contract_id=self.contract_id,
                parameter_id=self.parameter_id,
                revoked_at__isnull=True,
            )
            .first()
        )

        if assignment is None:
            raise NotFound(
                "No active assignment exists for this contract and parameter."
            )

        assignment.revoked_at = timezone.now()
        assignment.revoked_by = self.actor
        assignment.save(update_fields=["revoked_at", "revoked_by"])

        return assignment