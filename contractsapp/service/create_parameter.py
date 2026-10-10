from django.db import IntegrityError, transaction
from rest_framework.exceptions import PermissionDenied, ValidationError

from ..models import ParameterModel


class CreateParameterService:
    def __init__(self, actor, validated_data):
        self.actor = actor
        self.validated_data = validated_data

    @transaction.atomic
    def execute(self):
        if not self.actor.has_perm("locationsapp.add_parametermodel"):
            raise PermissionDenied(
                "You do not have permission to create parameters."
            )

        try:
            parameter = ParameterModel.objects.create(
                **self.validated_data
            )
        except IntegrityError as exc:
            raise ValidationError(
                "A parameter with this name already exists."
            ) from exc

        return parameter