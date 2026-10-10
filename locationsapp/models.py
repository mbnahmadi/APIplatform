from django.db import models
from django.contrib.auth import get_user_model
from contractsapp.models import ContractModel
from django.conf import settings

# from contractsapp.models import ContractModel


User = get_user_model()

# Create your models here.
class PointModel(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    latitude = models.DecimalField(
        max_digits=7,
        decimal_places=4,
    )

    longitude = models.DecimalField(
        max_digits=7,
        decimal_places=4,
    )
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["latitude", "longitude"],
                name="unique_latlon",
            ),
        ]

        permissions = [
            ("create_point", "Can create point"),
        ]

    def __str__(self):
        return f"{self.name}: {self.latitude}-{self.longitude}"


class ContractPointModel(models.Model):
    contract = models.ForeignKey(
        ContractModel,
        on_delete=models.CASCADE,
        related_name="contract_points",
    )
    point = models.ForeignKey(
        PointModel,
        on_delete=models.PROTECT,
        related_name="contract_points",
    )
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="point_assignments_created",
    )
    assigned_at = models.DateTimeField(auto_now_add=True)

    revoked_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    revoked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="point_assignments_revoked",
    )

    class Meta:
        permissions = [
            ("assign_point", "Can assign point to contract"),
            ("remove_point", "Can revoke point assignment"),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["contract", "point"],
                condition=models.Q(revoked_at__isnull=True),
                name="unique_active_contract_point",
            ),
        ]

    @property
    def is_active(self):
        return self.revoked_at is None

# class UserPointModel(models.Model):
#     user = models.ForeignKey(
#         User,
#         on_delete=models.PROTECT,
#         related_name="user_points",
#     )

#     point = models.ForeignKey(
#         PointModel,
#         on_delete=models.CASCADE,
#         related_name="user_points",
#     )

#     assigned_at = models.DateTimeField(
#         auto_now_add=True,
#     )

#     assigned_by = models.ForeignKey(
#         User,
#         on_delete=models.PROTECT,
#         related_name="point_assignments_created",
#     )

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=["user", "point"],
#                 name="unique_user_point",
#             ),
#         ]

#     def __str__(self):
#         return f"{self.user} -> {self.point} (by {self.assigned_by})"