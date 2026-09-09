from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class ContractModel(models.Model):

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
    used_requests = models.PositiveIntegerField(default=0)
    rate_limit = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(end_date__gt=models.F("start_date")),
                name="contract_end_after_start",
            ),
            models.CheckConstraint(
                condition=models.Q(rate_limit__gt=0),
                name="contract_rate_limit_gt_zero",
            ),
            models.CheckConstraint(
                condition=models.Q(request_quota__gt=0),
                name="contract_request_quota_gt_zero",
            ),
            models.CheckConstraint(
                condition=models.Q(request_quota__gte=models.F("used_requests")),
                name="contract_quota_gte_used_requests",
            )
        ]

    def __str__(self):
        return f"{self.user} | {self.start_date} to {self.end_date}"



class ParameterModel(models.Model):
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
        return f"{self.name} ({self.unit})"


class ContractParameterModel(models.Model):
    contract = models.ForeignKey(
        ContractModel,
        on_delete=models.CASCADE,
        related_name="contract_parameters"
        )
    parameter = models.ForeignKey(
        ParameterModel,
        on_delete=models.PROTECT,
        related_name="contract_parameters",
    )
    assigned_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="contract_parameter_assignments_created"
    )
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["contract", "parameter"],
                name="unique_contract_parameter",
            ),
        ]

    def __str__(self):
        return f"{self.assigned_by} at {self.assigned_at}"
    

class APIKeyModel(models.Model):
    contract = models.ForeignKey(
        ContractModel,
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
       return f"{self.contract} - {'Active' if self.is_active else 'Inactive'}"



class ContractHistoryModel(models.Model):
    contract = models.ForeignKey(
        ContractModel,
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
        return f"{self.contract} - {self.field_name}: {self.old_value} -> {self.new_value}"