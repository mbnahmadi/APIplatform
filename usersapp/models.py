from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserModel(AbstractUser):
    class UserRole(models.TextChoices):
        ADMIN = "admin", "admin"
        CLIENT = "client", "client"
    email = models.EmailField(unique=True, null=False, blank=False)
    role = models.CharField(max_length=10, choices=UserRole.choices, default=UserRole.CLIENT)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "first_name", "last_name", "role"]

    def __str__(self):
        return f"{self.username} - {self.first_name} {self.last_name}"


class ClientProfileModel(models.Model):
    user = models.OneToOneField("UserModel", on_delete=models.CASCADE, related_name="client_profile")
    contract_start_date = models.DateTimeField(null=False, blank=False)
    contract_end_date = models.DateTimeField(null=False, blank=False)
    total_request_cap = models.PositiveIntegerField(null=False, blank=False)
    rate_limit_per_minutes = models.PositiveIntegerField(null=False, blank=False)

    def __str__(self):
        return f"{self.user.username} - {self.user.first_name} {self.user.last_name}"