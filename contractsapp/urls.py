from django.urls import path

from .views import (
    ContractCreateAPIView,
    ContractListAPIView,
    ContractRetrieveAPIView,
    ContractUpdateAPIView
)



urlpatterns = [
    path("contracts/", ContractCreateAPIView.as_view(), name="contract-create"),
    path("contracts/", ContractListAPIView.as_view(), name="contract-list"),
    path("contracts/<int:contract_id>/", ContractRetrieveAPIView.as_view(), name="contract-retrieve"),
    path("contracts/<int:contract_id>/", ContractUpdateAPIView.as_view(), name="contract-update"),

]