from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class Contract(models.Model):

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        INACTIVE = "INACTIVE", "Inactive"

    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="contracts",
    )

    start_date = models.DateField()
    end_date = models.DateField()

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    request_quota = models.PositiveIntegerField()
    rate_limit = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.start_date} to {self.end_date}"



class Parameter(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    unit = models.CharField(
        max_length=50,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return f"{self.name} - {self.unit} / {self.is_active}"


class APIKey(models.Model):
    contract = models.ForeignKey(
        Contract,
        on_delete=models.CASCADE,
        related_name="api_keys",
    )

    key_hash = models.CharField(
        max_length=64,
        unique=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    deactivated_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["contract"],
                condition=models.Q(is_active=True),
                name="unique_active_api_key_per_contract",
            ),
        ]

    def __str__(self):
        return f"{self.contract.user.first_name} - {self.is_active}"



class ContractHistory(models.Model):
    contract = models.ForeignKey(
        Contract,
        on_delete=models.CASCADE,
        related_name="history",
    )

    changed_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="contract_changes",
    )

    changed_at = models.DateTimeField(
        auto_now_add=True,
    )

    field_name = models.CharField(
        max_length=100,
    )

    old_value = models.TextField(
        null=True,
        blank=True,
    )

    new_value = models.TextField(
        null=True,
        blank=True,
    )
    def __str__(self):
        return f"{self.changed_by} at {self.changed_at}"