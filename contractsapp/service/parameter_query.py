from rest_framework.exceptions import PermissionDenied

from ..models import ParameterModel


class ParameterQueryService:
    def __init__(self, actor):
        self.actor = actor

    def get_queryset(self):
        if not self.actor.has_perm("locationsapp.view_parametermodel"):
            raise PermissionDenied(
                "You do not have permission to view parameters."
            )

        return ParameterModel.objects.all().order_by("id")

    def get_parameter(self, parameter_id):
        return self.get_queryset().filter(
            id=parameter_id
        ).first()