from rest_framework import serializers
from .models import ContractModel
from django.contrib.auth import get_user_model


User = get_user_model()

class ContractCreateSerializer(serializers.ModelSerializer):

    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="user",
    )

    class Meta:
        model = ContractModel
        fields = [
            "user_id",
            "start_date",
            "end_date",
            "request_quota",
            "rate_limit",
        ]

    def validate_user(self, user):
        if user.role != User.Role.CLIENT:
            raise serializers.ValidationError(
                "Contract can only be created for a client."
            )

        return user



class ContractSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContractModel
        fields = [
            "id",
            "user",
            "start_date",
            "end_date",
            "status",
            "request_quota",
            "used_requests",
            "rate_limit",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "status",
            "used_requests",
            "created_at",
            "updated_at",
        ]



class ContractUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractModel
        fields = [
            "start_date",
            "end_date",
            "request_quota",
            "rate_limit",
        ]


class ContractStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(
        choices=ContractModel.Status.choices
    )