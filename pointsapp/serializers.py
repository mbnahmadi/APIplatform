from rest_framework import serializers
from .models import UploadFileModel


class UploadFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadFileModel
        fields = ["file", "status", "error_message", "uploaded_at"]
        read_only_fields = ["status", "error_message", "uploaded_at"]

    def validate_file(self, value):
        if not value.name.endswith(".csv"):
            raise serializers.ValidationError({"file": "only csv files can uploaded."})
        return value
