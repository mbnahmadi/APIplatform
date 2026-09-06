from django.db import models
from usersapp.models import User
# Create your models here.

class UploadFileModel(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'pending'
        PROCESSING = 'processing', 'processing'
        COMPLETED = 'completed', 'completed'
        FAILED = 'failed', 'failed'
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="uploadfile")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='csv_import/%Y/%m/%d/')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    error_message = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File by {self.uploaded_by.username} at {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"


class UserPointModel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userpoints")
    name = models.CharField(max_length=100, null=False, blank=False)
    latitude = models.FloatField()
    longitude = models.FloatField()
    source_file = models.ForeignKey("UploadFileModel", on_delete=models.SET_NULL, null=True, blank=True, related_name="points")

    def __str__(self):
        return f"{self.name} ({self.latitude}, {self.longitude})"
