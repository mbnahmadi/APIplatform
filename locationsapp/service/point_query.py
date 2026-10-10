from rest_framework.exceptions import PermissionDenied
from ..models import PointModel


class PointQueryService:
    def __init__(self, actor):
        self.actor = actor

    def get_queryset(self):
        if not self.actor.has_perm("locationsapp.view_pointmodel"):
            raise PermissionDenied(
                "You do not have permission to view points."
            )

        return PointModel.objects.all().order_by("id")

    def get_point(self, point_id):
        return self.get_queryset().filter(id=point_id).first()