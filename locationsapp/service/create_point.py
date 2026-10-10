from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework.exceptions import PermissionDenied, ValidationError

from ..models import PointModel


class CreatePointService:
    def __init__(self, actor, validated_data):
        self.actor = actor
        self.validated_data = validated_data

    @transaction.atomic
    def execute(self):
        if not self.actor.has_perm("locationsapp.create_point"):
            raise PermissionDenied(
                "You do not have permission to create points."
            )

        try:
            point = PointModel.objects.create(
                **self.validated_data
            )
        except IntegrityError as exc:
            raise ValidationError(
                "A point with this name or coordinates already exists."
            ) from exc

        return point