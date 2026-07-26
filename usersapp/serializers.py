from rest_framework import serializers
from .models import UserModel, ClientProfileModel

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = UserModel
        fields = ["username", "password", "email", "first_name", "last_name", "role", "is_active"]

    def create(self, validated_data):
        return UserModel.objects.create_user(
            username = validated_data["username"],
            password = validated_data["password"],
            email = validated_data["email"],
            first_name = validated_data["first_name"],
            last_name = validated_data["last_name"],
            role = validated_data["role"],
            is_active = validated_data["is_active"]
        )


class ClientProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = ClientProfileModel
        fields = ["user", "contract_start_date", "contract_end_date", "total_request_cap", "rate_limit_per_minutes"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")

        user_data = UserModel.objects.create_user(
            username = user_data["username"],
            password = user_data["password"],
            email = user_data["email"],
            first_name = user_data["first_name"],
            last_name = user_data["last_name"],
            role = user_data["role"],
            is_active = user_data["is_active"]
        )
        client_profile = ClientProfileModel.objects.create(user=user_data, **validated_data)

        return client_profile

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if user_data is not None:
            user_instance = (
                
                instance.user
            )  # Access the User object linked via Foreign Key
            for attr, value in user_data.items():
                setattr(user_instance, attr, value)
            user_instance.save()

        return instance







