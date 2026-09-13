from django.shortcuts import render
# from .models import 
from .serializers import (
    UserLoginSerializer, 
    UserSerializer, 
    UserCreateSerializer, 
    AssignPermissionSerializer, 
    UserUpdateSerializer, 
    UserStatusSerializer,
    UserRoleSerializer,
    )
from .permissions import IsAdminUser, CanViewUsers, CanManagePermissions
from .service.assign_permissions import AssignPermissionService
from .service.change_user_role import ChangeUserRoleService
# from .service.api_token import GenerateApiKeyService

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.shortcuts import get_object_or_404

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from drf_spectacular.utils import extend_schema
# Create your views here.

User = get_user_model()


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


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    refresh["user_id"] = user.id
    refresh["role"] = user.role

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

        

class UserListAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        CanViewUsers,
    ]

    def get(self, request):
        users = User.objects.all()

        serializer = UserSerializer(users, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class UserCreateAPIView(APIView):

    authentication_classes = [
        JWTAuthentication,
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
        JWTAuthentication,
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


class UserUpdateAPIView(APIView):

    authentication_classes = [
        JWTAuthentication,
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


class UserStatusAPIView(APIView):

    authentication_classes = [
        JWTAuthentication,
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



class ChangeUserRoleAPIView(APIView):

    authentication_classes = [
        JWTAuthentication,
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