from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError

from contractsapp.models import ContractModel
from ..models import ContractParameterModel, ParameterModel


class ChangeParameterStatusService:
    def __init__(self, actor, parameter_id, is_active):
        self.actor = actor
        self.parameter_id = parameter_id
        self.is_active = is_active

    @transaction.atomic
    def execute(self):
        if not self.actor.has_perm("contractsapp.change_parameter_status"):
            raise PermissionDenied(
                "You do not have permission to change parameter status."
            )

        parameter = (
            ParameterModel.objects
            .select_for_update()
            .filter(pk=self.parameter_id)
            .first()
        )

        if parameter is None:
            raise NotFound("Parameter not found.")

        # اگر پارامتر از قبل در وضعیت درخواستی است، تغییری لازم نیست.
        if parameter.is_active == self.is_active:
            return parameter

        if not self.is_active:
            today = timezone.localdate()

            has_active_contract_assignment = (
                ContractParameterModel.objects
                .filter(
                    parameter=parameter,
                    revoked_at__isnull=True,
                    contract__status=ContractModel.Status.ACTIVE,
                    contract__start_date__lte=today,
                    contract__end_date__gte=today,
                )
                .exists()
            )

            if has_active_contract_assignment:
                raise ValidationError(
                    "Cannot deactivate a parameter assigned to a currently valid contract."
                )

        parameter.is_active = self.is_active
        parameter.save(update_fields=["is_active"])

        return parameter