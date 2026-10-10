from rest_framework import serializers

from .models import PointModel


class PointCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointModel
        fields = [
            "name",
            "latitude",
            "longitude",
        ]



class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointModel
        fields = ["id", "name", "latitude", "longitude"]
        read_only_fields = fields


class AssignPointSerializer(serializers.Serializer):
    point_id = serializers.IntegerField(min_value=1)