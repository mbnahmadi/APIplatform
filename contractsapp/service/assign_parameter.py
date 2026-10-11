from django.db import IntegrityError, transaction
from django.utils import timezone
from rest_framework.exceptions import (
    NotFound,
    PermissionDenied,
    ValidationError,
)

from contractsapp.models import ContractModel
from ..models import ParameterModel, ContractParameterModel


class AssignParameterService:
    def __init__(self, actor, contract_id, parameter_id):
        self.actor = actor
        self.contract_id = contract_id
        self.parameter_id = parameter_id

    @transaction.atomic
    def execute(self):
        if not self.actor.has_perm("contractsapp.assign_parameter"):
            raise PermissionDenied(
                "You do not have permission to assign parameters."
            )

        contract = ContractModel.objects.filter(
            pk=self.contract_id
        ).first()

        if contract is None:
            raise NotFound("Contract not found.")

        today = timezone.localdate()

        if contract.status != ContractModel.Status.ACTIVE:
            raise ValidationError(
                "Cannot assign parameters to an inactive contract."
            )

        if contract.end_date < today:
            raise ValidationError(
                "Cannot assign parameters to an expired contract."
            )

        parameter = ParameterModel.objects.filter(
            pk=self.parameter_id,
            is_active=True,
        ).first()

        if parameter is None:
            raise NotFound("Active parameter not found.")

        try:
            assignment = ContractParameterModel.objects.create(
                contract=contract,
                parameter=parameter,
                assigned_by=self.actor,
            )
        except IntegrityError as exc:
            raise ValidationError(
                "This parameter is already assigned to this contract."
            ) from exc

        return assignment