from django.db import IntegrityError, transaction
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError

from contractsapp.models import ContractModel
from ..models import PointModel, ContractPointModel

from django.utils import timezone


class AssignPointService:
    def __init__(self, actor, contract_id, point_id):
        self.actor = actor
        self.contract_id = contract_id
        self.point_id = point_id

    @transaction.atomic
    def execute(self):
        if not self.actor.has_perm("locationsapp.assign_point"):
            raise PermissionDenied(
                "You do not have permission to assign points."
            )

        contract = ContractModel.objects.filter(
            pk=self.contract_id
        ).first()

        today = timezone.localdate()

        if contract.status != ContractModel.Status.ACTIVE:
            raise ValidationError("Cannot assign points to an inactive contract.")

        if contract.end_date < today:
            raise ValidationError(
                "Cannot assign points to an expired contract. Create a new contract."
            )


        if contract is None:
            raise NotFound("Contract not found.")

        point = PointModel.objects.filter(
            pk=self.point_id
        ).first()

        if point is None:
            raise NotFound("Point not found.")

        try:
            assignment = ContractPointModel.objects.create(
                contract=contract,
                point=point,
                assigned_by=self.actor,
            )
        except IntegrityError as exc:
            raise ValidationError(
                "This point is already assigned to this contract."
            ) from exc

        return assignment