from django.urls import path

from .views import (
    ContractCreateAPIView,
    ContractListAPIView,
    ContractRetrieveAPIView,
    ContractUpdateAPIView,
    ContractStatusAPIView,
    ContractRenewAPIView,
    ContractHistoryListAPIView,
    GenerateAPIKeyAPIView,
    RegenerateAPIKeyAPIView,
    ParameterCreateAPIView,
    ParameterListAPIView,
    ParameterDetailAPIView,
    AssignParameterAPIView,
    RevokeParameterAssignmentAPIView,
    ParameterStatusAPIView
)



urlpatterns = [
    path("contracts/", ContractCreateAPIView.as_view(), name="contract-create"),
    path("contracts-list/", ContractListAPIView.as_view(), name="contract-list"),
    path("contracts/<int:contract_id>/", ContractRetrieveAPIView.as_view(), name="contract-retrieve"),
    path("contracts/<int:contract_id>/", ContractUpdateAPIView.as_view(), name="contract-update"),
    path("contracts/<int:contract_id>/status/", ContractStatusAPIView.as_view(), name="contract-status"),
    path("contracts/<int:contract_id>/renew/", ContractRenewAPIView.as_view(), name="contract-renew"),
    path("contracts/<int:contract_id>/history/", ContractHistoryListAPIView.as_view(), name="contract-history"),

    path("api-key/generate/", GenerateAPIKeyAPIView.as_view(), name="generate-apikey"),
    path("api-key/regenerate/", RegenerateAPIKeyAPIView.as_view(), name="regenerate-apikey"),

    path("parameters/", ParameterCreateAPIView.as_view(), name="parameter-create"),
    path("parameters/", ParameterListAPIView.as_view(), name="parameter-list"),
    path("parameters/<int:id>/", ParameterDetailAPIView.as_view(), name="parameter-detail"),
    path("contracts/<int:contract_id>/parameters/", AssignParameterAPIView.as_view(), name="assign-parameter"),
    path("contracts/<int:contract_id>/parameters/<int:parameter_id>/", RevokeParameterAssignmentAPIView.as_view(), name="revoke-parameter-assignment"),
    path("parameters/<int:parameter_id>/status/", ParameterStatusAPIView.as_view(), name="parameter-status"),


]