from rest_framework import serializers
# from .models import User
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import Permission
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.serializers import TokenRefreshSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["token_version"] = user.token_version
        return token


class VersionedTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        try:
            refresh = RefreshToken(attrs["refresh"])
        except TokenError:
            raise InvalidToken("Refresh token is invalid or expired.")

        user_id = refresh.get(api_settings.USER_ID_CLAIM)
        User = get_user_model()

        user = User.objects.filter(
            **{api_settings.USER_ID_FIELD: user_id}
        ).first()

        if (
            user is None
            or refresh.get("token_version") != user.token_version
        ):
            raise InvalidToken("Refresh token is no longer valid.")

        return super().validate(attrs)


class AssignPermissionSerializer(serializers.Serializer):

    permission_id = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(),
        source="permission",
    )



User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ["role", "email", "first_name", "last_name", "username", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            role=validated_data["role"],
            password=validated_data["password"]
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["role", "email", "first_name", "last_name", "username", "id", "is_active", "created_at", "updated_at"]

class UserFilterSerializer(serializers.Serializer):
    role = serializers.ChoiceField(
        choices=User.Role.choices,
        required=False,
    )

class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "username",
        ]

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance


        
class UserLoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        request = self.context.get("request")

        user = authenticate(
            request=request,
            identifier=attrs["identifier"],
            password=attrs["password"],
        )

        if user is None:
            raise serializers.ValidationError(
                "Invalid username/email or password."
            )

        attrs["user"] = user
        return attrs



class UserStatusSerializer(serializers.Serializer):
    is_active = serializers.BooleanField()


class UserRoleSerializer(serializers.Serializer):
    role = serializers.ChoiceField(
        choices=User.Role.choices
    )


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class MyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
        ]
        read_only_fields = fields

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
        ]



class ClientChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )
    new_password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )
    confirm_new_password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )

    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_new_password"]:
            raise serializers.ValidationError({
                "confirm_new_password": "Passwords do not match."
            })

        user = self.context["user"]

        if not user.check_password(attrs["current_password"]):
            raise serializers.ValidationError({
                "current_password": "Current password is incorrect."
            })

        validate_password(attrs["new_password"], user=user)

        return attrs


class AdminChangeClientPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )
    confirm_new_password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )

    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_new_password"]:
            raise serializers.ValidationError({
                "confirm_new_password": "Passwords do not match."
            })

        validate_password(
            attrs["new_password"],
            user=self.context["user"],
        )

        return attrs

# class LogoutSerializer(serializers.Serializer):
#     refresh = serializers.CharField()


# class UserSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#     class Meta:
#         model = User
#         fields = ["id", "username", "password", "email", "first_name", "last_name", "role", "is_active"]

#     def create(self, validated_data):
#         return User.objects.create_user(
#             username = validated_data["username"],
#             password = validated_data["password"],
#             email = validated_data["email"],
#             first_name = validated_data["first_name"],
#             last_name = validated_data["last_name"],
#             role = validated_data["role"],
#             is_active = validated_data["is_active"]
#         )
        


# class ClientProfileSerializer(serializers.ModelSerializer):
#     user = UserSerializer()
#     class Meta:
#         model = ClientProfileModel
#         fields = ["user", "contract_start_date", "contract_end_date", "total_request_cap", "rate_limit_per_minutes"]
#         # read_only_fields = [""]

#     def create(self, validated_data):
#         user_data = validated_data.pop("user")

#         user_data = User.objects.create_user(
#             username = user_data["username"],
#             password = user_data["password"],
#             email = user_data["email"],
#             first_name = user_data["first_name"],
#             last_name = user_data["last_name"],
#             role = user_data["role"],
#             is_active = user_data["is_active"]
#         )
#         client_profile = ClientProfileModel.objects.create(user=user_data, **validated_data)

#         return client_profile

#     def update(self, instance, validated_data):
#         user_data = validated_data.pop('user', None)
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()
#         if user_data is not None:
#             user_instance = (
                
#                 instance.user
#             )  # Access the User object linked via Foreign Key
#             for attr, value in user_data.items():
#                 setattr(user_instance, attr, value)
#             user_instance.save()

#         return instance



# class GenerateApiKeyResponseSerializer(serializers.Serializer):
#     api_key = serializers.CharField(read_only=True)
