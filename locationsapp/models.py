from django.db import models
from django.contrib.auth import get_user_model
from contractsapp.models import ContractModel

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
        User,
        on_delete=models.PROTECT,
        related_name="contract_point_assignments_created",
    )
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["contract", "point"],
                name="unique_contract_point",
            ),
        ]

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