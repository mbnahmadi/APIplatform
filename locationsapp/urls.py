from django.urls import path

from .views import (
    PointCreateAPIView,
    PointListAPIView,
    PointDetailAPIView,
    AssignPointAPIView,
    RemovePointAPIView
)



urlpatterns = [
    path("points/",PointCreateAPIView.as_view(),name="point-create"),
    path("points-list/", PointListAPIView.as_view(), name="point-list"),
    path("points/<int:id>/", PointDetailAPIView.as_view(), name="point-detail"),
    path("contracts/<int:contract_id>/points/", AssignPointAPIView.as_view(), name="assign-point"),
    path("point-assignment-revoke/contracts/<int:contract_id>/points/<int:point_id>/", RemovePointAPIView.as_view(), name="remove-point"),
]