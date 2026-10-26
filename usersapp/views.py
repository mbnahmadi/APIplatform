from django.shortcuts import render
# from .authentication import VersionedJWTAuthentication
from usersapp.authentication import VersionedJWTAuthentication
# from .models import 
from .serializers import (
    UserLoginSerializer, 
    UserSerializer, 
    UserCreateSerializer, 
    AssignPermissionSerializer, 
    UserUpdateSerializer, 
    UserStatusSerializer,
    UserRoleSerializer,
    LogoutSerializer,
    UserFilterSerializer,
    MyProfileSerializer,
    UserProfileUpdateSerializer,
    AdminChangeClientPasswordSerializer,
    ClientChangePasswordSerializer,
    CustomTokenObtainPairSerializer,
    VersionedTokenRefreshSerializer
    )
from .permissions import IsAdminUser, CanViewUsers, CanManagePermissions
from .service.assign_permissions import AssignPermissionService
from .service.change_user_role import ChangeUserRoleService
from .service.logout import LogoutService
from .service.update_user_profile import UpdateUserProfileService
from .service.change_own_password import ChangeOwnPasswordService
from .service.admin_change_client_password import AdminChangeClientPasswordService
# from .service.api_token import GenerateApiKeyService

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.shortcuts import get_object_or_404

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

# from rest_framework_simplejwt.authentication import VersionedJWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

# from rest_framework_simplejwt.views import TokenObtainPairView


from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
# Create your views here.

User = get_user_model()



# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer
class VersionedTokenRefreshView(TokenRefreshView):
    serializer_class = VersionedTokenRefreshSerializer


class PermissionListAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        CanManagePermissions,
    ]

    def get(self, request):
        permissions = Permission.objects.filter(
            content_type__app_label__in=[
                "usersapp",
                "contractsapp",
                "locationsapp",
            ],
        ).order_by(
            "content_type__app_label",
            "codename",
        )

        data = [
            {
                "id": permission.id,
                "name": permission.name,
                "codename": permission.codename,
                "app_label": permission.content_type.app_label,
            }
            for permission in permissions
        ]

        return Response(
            data,
            status=status.HTTP_200_OK,
        )


@extend_schema(request=AssignPermissionSerializer)
class UserPermissionAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request, user_id):

        target_user = get_object_or_404(
            User,
            pk=user_id,
        )

        serializer = AssignPermissionSerializer(
            data=request.data,
        )

        serializer.is_valid(raise_exception=True)

        permission = serializer.validated_data["permission"]

        try:
            AssignPermissionService(
                actor=request.user,
                target_user=target_user,
                permission=permission,
            ).execute()

        except ValueError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except PermissionDenied as exc:
            raise PermissionDenied(str(exc))

        return Response(
            {
                "detail": "Permission assigned successfully."
            },
            status=status.HTTP_201_CREATED,
        )



class UserPermissionListAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request, user_id):

        if not request.user.has_perm(
            "usersapp.manage_permissions"
        ):
            raise PermissionDenied(
                "You do not have permission to manage permissions."
            )

        target_user = get_object_or_404(
            User,
            pk=user_id,
        )

        if target_user.role != User.Role.ADMIN:
            raise PermissionDenied(
                "Permissions can only be viewed for admins."
            )

        permissions = target_user.user_permissions.select_related(
            "content_type"
        ).all()

        data = [
            {
                "id": permission.id,
                "name": permission.name,
                "codename": permission.codename,
                "app_label": permission.content_type.app_label,
            }
            for permission in permissions
        ]

        return Response(
            data,
            status=status.HTTP_200_OK,
        )


class MyProfileAPIView(APIView):
    authentication_classes = [VersionedJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = MyProfileSerializer(request.user)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class UserProfileAPIView(APIView):
    authentication_classes = [VersionedJWTAuthentication]
    permission_classes = [
        IsAuthenticated,
        CanViewUsers,
    ]

    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)

        serializer = MyProfileSerializer(user)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

@extend_schema(request=UserProfileUpdateSerializer)
class UserProfileUpdateAPIView(APIView):
    authentication_classes = [VersionedJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, user_id):
        if not request.user.has_perm("usersapp.change_user_profile"):
            raise PermissionDenied(
                "You do not have permission to change user profiles."
            )

        serializer = UserProfileUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = UpdateUserProfileService(
            actor=request.user,
            user_id=user_id,
            validated_data=serializer.validated_data,
        ).execute()

        response_serializer = MyProfileSerializer(user)

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK,
        )

class MyPermissionListAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):
        user = request.user

        if user.role != User.Role.ADMIN:
            raise PermissionDenied(
                "Only admins can view their own permissions."
            )

        permissions = user.user_permissions.select_related(
            "content_type"
        ).all()

        data = [
            {
                "id": permission.id,
                "name": permission.name,
                "codename": permission.codename,
                "app_label": permission.content_type.app_label,
            }
            for permission in permissions
        ]

        return Response(
            data,
            status=status.HTTP_200_OK,
        )

class UserPermissionDeleteAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def delete(self, request, user_id, permission_id):

        if not request.user.has_perm(
            "usersapp.manage_permissions"
        ):
            raise PermissionDenied(
                "You do not have permission to manage permissions."
            )

        target_user = get_object_or_404(
            User,
            pk=user_id,
        )

        if target_user.role != User.Role.ADMIN:
            raise PermissionDenied(
                "Permissions can only be managed for admins."
            )

        if request.user.pk == target_user.pk:
            raise PermissionDenied(
                "You cannot manage your own permissions."
            )

        permission = get_object_or_404(
            Permission,
            pk=permission_id,
        )

        if (
            permission.content_type.app_label == "usersapp"
            and permission.codename == "manage_permissions"
        ):
            raise PermissionDenied(
                "This permission cannot be managed."
            )

        if not target_user.user_permissions.filter(
            pk=permission.pk
        ).exists():
            return Response(
                {
                    "detail": "This user does not have this permission."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        target_user.user_permissions.remove(permission)

        return Response(
            {
                "detail": "Permission removed successfully."
            },
            status=status.HTTP_200_OK,
        )
# ==================================================================


# def get_tokens_for_user(user):
#     refresh = RefreshToken.for_user(user)

#     refresh["user_id"] = user.id
#     refresh["role"] = user.role

#     return {
#         "refresh": str(refresh),
#         "access": str(refresh.access_token),
#     }
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    refresh["token_version"] = user.token_version

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


@extend_schema(request=UserLoginSerializer)
class LoginAPIView(APIView):
    def post(self, request):
        # identifier = request.POST.get("identifier")
        # password = request.POST.get("password")
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.validated_data["user"]
            token = get_tokens_for_user(user)
            return Response(token, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(request=LogoutSerializer)
class LogoutAPIView(APIView):
    authentication_classes = [VersionedJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = LogoutService(
            refresh_token=serializer.validated_data["refresh"]
        ).execute()

        return Response(result, status=status.HTTP_200_OK)



@extend_schema(
    summary="List of users",
    description=(
        "Retrieve a list of users. You can optionally filter the results "
        "by user role using the `role` query parameter. "
        "Supported values are `ADMIN` and `CLIENT`. "
        "If the parameter is omitted, all users are returned."
    ),
    parameters=[
        OpenApiParameter(
            name="role",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
            enum=["ADMIN", "CLIENT"],
            description="Filter users by role. Allowed values: ADMIN, CLIENT.",
        ),
    ],
    responses=UserSerializer(many=True),
)
class UserListAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        CanViewUsers,
    ]

    def get(self, request):
        filter_serializer = UserFilterSerializer(
            data=request.query_params
        )
        filter_serializer.is_valid(raise_exception=True)

        users = User.objects.all()

        role = filter_serializer.validated_data.get("role")

        if role:
            users = users.filter(role=role)

        serializer = UserSerializer(users, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


@extend_schema(request=UserCreateSerializer)
class UserCreateAPIView(APIView):

    authentication_classes = [
        VersionedJWTAuthentication,
    ]

    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):
        serializer = UserCreateSerializer(
            data=request.data,
        )

        serializer.is_valid(raise_exception=True)

        role = serializer.validated_data["role"]

        if role == User.Role.CLIENT:
            if not request.user.has_perm("users.create_client"):
                raise PermissionDenied

        elif role == User.Role.ADMIN:
            if not request.user.has_perm("users.create_admin"):
                raise PermissionDenied

        user = serializer.save()

        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )


class UserRetrieveAPIView(APIView):

    authentication_classes = [
        VersionedJWTAuthentication,
    ]

    permission_classes = [
        IsAuthenticated,
        CanViewUsers,
    ]

    def get(self, request, user_id):

        user = get_object_or_404(
            User,
            pk=user_id,
        )

        serializer = UserSerializer(user)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


@extend_schema(request=UserUpdateSerializer)
class UserUpdateAPIView(APIView):

    authentication_classes = [
        VersionedJWTAuthentication,
    ]

    permission_classes = [
        IsAuthenticated,
    ]

    def patch(self, request, user_id):

        user = get_object_or_404(
            User,
            pk=user_id,
        )

        if user.role == User.Role.CLIENT:
            if not request.user.has_perm(
                "users.update_client"
            ):
                raise PermissionDenied

        elif user.role == User.Role.ADMIN:
            if not request.user.has_perm(
                "users.update_admin"
            ):
                raise PermissionDenied

        serializer = UserUpdateSerializer(
            user,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.save()

        return Response(
            UserSerializer(user).data,
            status=status.HTTP_200_OK,
        )


@extend_schema(request=UserStatusSerializer)
class UserStatusAPIView(APIView):

    authentication_classes = [
        VersionedJWTAuthentication,
    ]

    permission_classes = [
        IsAuthenticated,
    ]

    def patch(self, request, user_id):

        user = get_object_or_404(
            User,
            pk=user_id,
        )

        if user.role == User.Role.CLIENT:
            if not request.user.has_perm(
                "users.activate_client"
            ):
                raise PermissionDenied

        elif user.role == User.Role.ADMIN:
            if not request.user.has_perm(
                "users.activate_admin"
            ):
                raise PermissionDenied

        serializer = UserStatusSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True
        )

        user.is_active = serializer.validated_data[
            "is_active"
        ]
        user.save(update_fields=["is_active"])

        return Response(
            UserSerializer(user).data,
            status=status.HTTP_200_OK,
        )


@extend_schema(request=UserRoleSerializer)
class ChangeUserRoleAPIView(APIView):

    authentication_classes = [
        VersionedJWTAuthentication,
    ]

    permission_classes = [
        IsAuthenticated,
    ]

    def patch(self, request, user_id):

        target_user = get_object_or_404(
            User,
            pk=user_id,
        )

        serializer = UserRoleSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True
        )

        service = ChangeUserRoleService(
            actor=request.user,
            target_user=target_user,
            new_role=serializer.validated_data["role"],
        )

        user = service.execute()

        return Response(
            UserSerializer(user).data,
            status=status.HTTP_200_OK,
        )


@extend_schema(request=ClientChangePasswordSerializer)
class ChangeOwnPasswordAPIView(APIView):
    authentication_classes = [VersionedJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ClientChangePasswordSerializer(
            data=request.data,
            context={"user": request.user},
        )
        serializer.is_valid(raise_exception=True)

        ChangeOwnPasswordService(
            actor=request.user,
            new_password=serializer.validated_data["new_password"],
        ).execute()

        return Response(
            {"detail": "Password changed successfully."},
            status=status.HTTP_200_OK,
        )

@extend_schema(request=AdminChangeClientPasswordSerializer)
class AdminChangeClientPasswordAPIView(APIView):
    authentication_classes = [VersionedJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        target_user = get_object_or_404(User, pk=user_id)

        serializer = AdminChangeClientPasswordSerializer(
            data=request.data,
            context={"user": target_user},
        )
        serializer.is_valid(raise_exception=True)

        AdminChangeClientPasswordService(
            actor=request.user,
            user_id=user_id,
            new_password=serializer.validated_data["new_password"],
        ).execute()

        return Response(
            {"detail": "Client password changed successfully."},
            status=status.HTTP_200_OK,
        )


    
# @extend_schema(request=LogoutSerializer)
# class LogoutAPIView(APIView):
#     def post(self, request):
#         serializer = LogoutSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         refresh_token  = serializer.validated_data["refresh"]
        
#         try:
#             # the library can decode and validate that specific token
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#             return Response(status=status.HTTP_205_RESET_CONTENT)
#         except (InvalidToken, TokenError) as e:
#             return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)


# class UserCreateView(generics.CreateAPIView):
#     queryset = ClientProfileModel.objects.all()
#     serializer_class = ClientProfileSerializer
#     permission_classes = [IsAdminUser]

# class UserRetreiveView(generics.ListAPIView):
#     queryset = ClientProfileModel.objects.all()
#     serializer_class = ClientProfileSerializer
#     permission_classes = [IsAdminUser]


# class UserRetreiveUpdateView(generics.RetrieveUpdateAPIView):
#     queryset = ClientProfileModel.objects.all()
#     serializer_class = ClientProfileSerializer
#     permission_classes = [IsAdminUser]


# class UserDeleteView(generics.DestroyAPIView):
#     queryset = ClientProfileModel.objects.all()
#     serializer_class = ClientProfileSerializer
#     permission_classes = [IsAdminUser]

#     def perform_destroy(self, instance):
#         user = getattr(instance, "user", None)
#         instance.delete()
#         if user:
#             user.delete()

# # ================ client ================
# class ClientProfileView(generics.RetrieveAPIView):
#     serializer_class = ClientProfileSerializer
#     # def get_queryset(self):
#     #     return ClientProfileModel.objects.filter(user=self.request.user)
#     def get_object(self):
#         return generics.get_object_or_404(ClientProfileModel, user=self.request.user)


# # ============= API token =======================
# class GenerateAPIToken(APIView):
#     def post(self, request):
#         key = GenerateApiKeyService(user=request.user)
#         api_key = key.execute()

#         serializer = GenerateApiKeyResponseSerializer({"api_key": api_key})
#         # if serializer.is_valid():
#         return Response(serializer.data)
#         # return Response({"error": "bad request"})