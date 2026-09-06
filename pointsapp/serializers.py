# from rest_framework import serializers
# from .models import UploadFileModel, UserPointModel


# class UploadFileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UploadFileModel
#         fields = ["owner", "uploaded_by", "file", "status", "error_message", "uploaded_at"]
#         read_only_fields = ["uploaded_by", "status", "error_message", "uploaded_at"]

#     def validate_file(self, value):
#         if not value.name.endswith(".csv"):
#             raise serializers.ValidationError({"file": "only csv files can uploaded."})
#         return value

# class PointSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserPointModel
#         fields = ["id", "owner", "name", "latitude", "longitude"]
#         read_only_fields = ["owner"]