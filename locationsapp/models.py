from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Point(models.Model):
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
        return f"{self.name}: {self.longitude}-{self.longitude}"


class UserPoint(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_points",
    )

    point = models.ForeignKey(
        Point,
        on_delete=models.CASCADE,
        related_name="user_points",
    )

    assigned_at = models.DateTimeField(
        auto_now_add=True,
    )

    assigned_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="point_assignments_created",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "point"],
                name="unique_user_point",
            ),
        ]

    def __str__(self):
        return f"{self.assigned_by} at {self.assigned_at}"