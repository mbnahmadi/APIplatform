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
from .views import (DocumentListCreateView, 
                    PointListView, 
                    PointCreateView, 
                    PointdeleteView, 
                    PointRetrieveUpdateView, 
                    ClientPointView,
                    WeatherTestView
)

urlpatterns = [
    path("admin/points/upload/", DocumentListCreateView.as_view(), name="uploadfile"),
    path("admin/points/list/user/<int:user>/", PointListView.as_view(), name="pointlist"),
    path("admin/points/create/user/<int:user>/", PointCreateView.as_view(), name="pointcreate"),
    path("admin/points/delete/user/<int:user>/point/<int:pk>/", PointdeleteView.as_view(), name="pointdelete"),
    path("admin/points/update/user/<int:user>/point/<int:pk>/", PointRetrieveUpdateView.as_view(), name="pointupdate"),

    path("client/points/list/", ClientPointView.as_view(), name="clientpontlist"),


    path("test/", WeatherTestView.as_view(), name="test"),
]
