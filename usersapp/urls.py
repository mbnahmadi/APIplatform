"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    LoginAPIView,
    UserListAPIView, 
    UserCreateAPIView, 
    PermissionListAPIView, 
    UserPermissionAPIView, 
    UserPermissionListAPIView,
    UserPermissionDeleteAPIView,
    UserRetrieveAPIView,
    UserUpdateAPIView,
    UserStatusAPIView
)

urlpatterns = [
    path("auth/login/", LoginAPIView.as_view(), name='login'),
    path("users/", UserListAPIView.as_view(), name='retrieve-users'),
    path("users/<int:user_id>/", UserRetrieveAPIView.as_view(), name="user-retrieve"),
    path("users/create/", UserCreateAPIView.as_view(), name="user-create"),
    path("users/<int:user_id>/", UserUpdateAPIView.as_view(), name="user-update"),
    path("users/<int:user_id>/status/", UserStatusAPIView.as_view(), name="user-status"),

    path("permissions/", PermissionListAPIView.as_view(), name="permissions-llist"),
    path("users/<int:user_id>/permissions/", UserPermissionAPIView.as_view(), name="user-permission"),
    path("users/<int:user_id>/permissions/", UserPermissionListAPIView.as_view(), name="user-permission-list"),
    path("users/<int:user_id>/permissions/<int:permission_id>/", UserPermissionDeleteAPIView.as_view(), name="user-permission-delete"),

    # path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('logout/', LogoutAPIView.as_view(), name='logout'),

    # path('admin/users/list/', UserRetreiveView.as_view(), name='users-list'),
    # path('admin/users/create/', UserCreateView.as_view(), name='users-create'),
    # path('admin/users/update/<int:pk>/', UserRetreiveUpdateView.as_view(), name='users-update'),
    # path('admin/users/<int:pk>/delete/', UserDeleteView.as_view(), name='users-delete'),

    # path('profile/', ClientProfileView.as_view(), name='clientprofile'),

    # path('api-token/', GenerateAPIToken.as_view(), name='api-token'),



]
