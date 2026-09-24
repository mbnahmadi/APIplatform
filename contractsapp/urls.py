from django.urls import path

from .views import (
    ContractCreateAPIView,
    ContractListAPIView,
    ContractRetrieveAPIView,
    ContractUpdateAPIView,
    ContractStatusAPIView,
    ContractRenewAPIView,
    ContractHistoryListAPIView
)



urlpatterns = [
    path("contracts/", ContractCreateAPIView.as_view(), name="contract-create"),
    path("contracts/", ContractListAPIView.as_view(), name="contract-list"),
    path("contracts/<int:contract_id>/", ContractRetrieveAPIView.as_view(), name="contract-retrieve"),
    path("contracts/<int:contract_id>/", ContractUpdateAPIView.as_view(), name="contract-update"),
    path("contracts/<int:contract_id>/status/", ContractStatusAPIView.as_view(), name="contract-status"),
    path("contracts/<int:contract_id>/renew/", ContractRenewAPIView.as_view(), name="contract-renew"),
    path("contracts/<int:contract_id>/history/", ContractHistoryListAPIView.as_view(), name="contract-history"),

]