import secrets
from hashlib import sha256
from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth import get_user_model
from django.conf import settings
# Create your models here.

class User(AbstractUser):

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        CLIENT = "CLIENT", "Client"

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.CLIENT
    )
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} - {self.first_name} {self.last_name}"






# API_KEY_PREFIX = settings.API_KEY_PREFIX 


# class UserModel(AbstractUser):
#     class UserRole(models.TextChoices):
#         ADMIN = "admin", "admin"
#         CLIENT = "client", "client"
#     email = models.EmailField(unique=True, null=False, blank=False)
#     role = models.CharField(max_length=10, choices=UserRole.choices, default=UserRole.CLIENT)

#     USERNAME_FIELD = "username"
#     REQUIRED_FIELDS = ["email", "first_name", "last_name", "role"]

#     def __str__(self):
#         return f"{self.username} - {self.first_name} {self.last_name}"

# # User = get_user_model()
# class ClientProfileModel(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="client_profile")
#     contract_start_date = models.DateTimeField(null=False, blank=False)
#     contract_end_date = models.DateTimeField(null=False, blank=False)
#     total_request_cap = models.PositiveIntegerField(null=False, blank=False)
#     rate_limit_per_minutes = models.PositiveIntegerField(null=False, blank=False)

#     def __str__(self):
#         return f"{self.user.username} - {self.user.first_name} {self.user.last_name}"


# class APITokenModel(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="api_token")
#     created_at = models.DateTimeField(auto_now_add=True)
#     token_hash = models.CharField(unique=True, max_length=64, db_index=True)
#     is_active = models.BooleanField(default=True)
#     last_used_at = models.DateTimeField(null=True, blank=True)

#     @staticmethod
#     def hash_token(api_key:str) -> str:
#         return sha256(api_key.encode('utf-8')).hexdigest()
    
#     def generate_token(self):
#         randon_part = secrets.token_urlsafe(32)
#         prefix = API_KEY_PREFIX
#         api_key = prefix + randon_part
#         self.token_hash = self.hash_token(api_key)
#         self.save() 
#         return api_key

#     @classmethod
#     def get_by_api_key(cls, api_key):
#         hashed_token = cls.hash_token(api_key)
#         return cls.objects.filter(token_hash=hashed_token).first()



#     def __str__(self):
#         return f"for {self.user.username} created at {self.created_at}"