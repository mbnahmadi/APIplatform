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
# from .views import LogoutAPIView, UserRetreiveView, UserRetreiveUpdateView, UserDeleteView, UserCreateView, ClientProfileView, GenerateAPIToken

urlpatterns = [
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
