from django.shortcuts import render
from django.shortcuts import render
# from .models import 
from .serializers import (
    ContractCreateSerializer,
    ContractSerializer,
    ContractUpdateSerializer,
    ContractStatusSerializer,
    ContractRenewSerializer,
    ContractHistorySerializer,
    APIKeySerializer,
    GenerateAPIKeySerializer,
    APIKeyStatusSerializer,
    ParameterCreateSerializer,
    ParameterSerializer,
    AssignParameterSerializer,
    ParameterStatusSerializer
    )

from .models import ContractModel, ContractHistoryModel, APIKeyModel
from .permissions import CanViewContracts, CanViewContractHistory
from .service.create_contract import CreateContractService
from .service.update_contract import UpdateContractService
# from .service.contract_status import ChangeContractStatusService
from .service.change_status_contract_history import ChangeContractStatusService
from .service.contract_renewal import RenewContractService
from .service.api_key_generate import GenerateAPIKeyService
from .service.api_key_regenerate import RegenerateAPIKeyService
from .service.api_key_revoke import RevokeAPIKeyService
from .service.create_parameter import CreateParameterService
from .service.parameter_query import ParameterQueryService
from .service.assign_parameter import AssignParameterService
from .service.revoke_parameter_assignment import RevokeParameterAssignmentService
from .service.change_parameter_status import ChangeParameterStatusService

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.shortcuts import get_object_or_404

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied


from rest_framework_simplejwt.authentication import JWTAuthentication


from drf_spectacular.utils import extend_schema
# Create your views here.


@extend_schema(request=ContractCreateSerializer)
class ContractCreateAPIView(APIView):

    authentication_classes = [
        JWTAuthentication,
    ]

    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):

        serializer = ContractCreateSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        contract = CreateContractService(
            actor=request.user,
            user=serializer.validated_data["user"],
            start_date=serializer.validated_data["start_date"],
            end_date=serializer.validated_data["end_date"],
            request_quota=serializer.validated_data["request_quota"],
            rate_limit=serializer.validated_data["rate_limit"],
        ).execute()

        return Response(
            ContractSerializer(contract).data,
            status=status.HTTP_201_CREATED,
        )


class ContractListAPIView(APIView):

    authentication_classes = [
        JWTAuthentication,
    ]

    permission_classes = [
        IsAuthenticated,
        CanViewContracts,
    ]

    def get(self, request):

        contracts = ContractModel.objects.select_related(
            "user"
        ).all()

        serializer = ContractSerializer(
            contracts,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )



class ContractRetrieveAPIView(APIView):
    authentication_classes = [
        JWTAuthentication,
    ]
    permission_classes = [
        IsAuthenticated,
        CanViewContracts,
    ]

    def get(self, request, contract_id):
        contract = get_object_or_404(
            ContractModel.objects.select_related("user"),
            pk=contract_id,
        )

        serializer = ContractSerializer(contract)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


@extend_schema(request=ContractUpdateSerializer)
class ContractUpdateAPIView(APIView):
    authentication_classes = [
        JWTAuthentication,
    ]
    permission_classes = [
        IsAuthenticated,
    ]

    def patch(self, request, contract_id):
        contract = get_object_or_404(
            ContractModel,
            pk=contract_id,
        )

        serializer = ContractUpdateSerializer(
            contract,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)

        contract = UpdateContractService(
            actor=request.user,
            contract=contract,
            validated_data=serializer.validated_data,
        ).execute()

        return Response(
            ContractSerializer(contract).data,
            status=status.HTTP_200_OK,
        )



@extend_schema(request=ContractStatusSerializer)
class ContractStatusAPIView(APIView):
    authentication_classes = [
        JWTAuthentication,
    ]
    permission_classes = [
        IsAuthenticated,
    ]

    def patch(self, request, contract_id):
        contract = get_object_or_404(
            ContractModel,
            pk=contract_id,
        )

        serializer = ContractStatusSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        contract = ChangeContractStatusService(
            actor=request.user,
            contract=contract,
            new_status=serializer.validated_data["status"],
        ).execute()

        return Response(
            ContractSerializer(contract).data,
            status=status.HTTP_200_OK,
        )



@extend_schema(request=ContractRenewSerializer)
class ContractRenewAPIView(APIView):
    authentication_classes = [
        JWTAuthentication,
    ]
    permission_classes = [
        IsAuthenticated,
    ]

    def patch(self, request, contract_id):
        contract = get_object_or_404(
            ContractModel,
            pk=contract_id,
        )

        serializer = ContractRenewSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        contract = RenewContractService(
            actor=request.user,
            contract=contract,
            validated_data=serializer.validated_data,
        ).execute()

        return Response(
            ContractSerializer(contract).data,
            status=status.HTTP_200_OK,
        )


class ContractHistoryListAPIView(APIView):
    authentication_classes = [
        JWTAuthentication,
    ]
    permission_classes = [
        IsAuthenticated,
        CanViewContractHistory,
    ]

    def get(self, request, contract_id):
        contract = get_object_or_404(
            ContractModel,
            pk=contract_id,
        )

        history = ContractHistoryModel.objects.filter(
            contract=contract
        ).select_related(
            "changed_by",
        ).order_by(
            "-changed_at"
        )

        serializer = ContractHistorySerializer(
            history,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


# =================== API Key ==============================
@extend_schema(request=GenerateAPIKeySerializer)
class GenerateAPIKeyAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GenerateAPIKeySerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        contract = get_object_or_404(
            ContractModel,
            pk=serializer.validated_data["contract_id"],
            user=request.user,
        )

        raw_key = GenerateAPIKeyService(
            actor=request.user,
            contract=contract,
        ).execute()

        response_serializer = APIKeySerializer(
            instance={"api_key": raw_key}
        )
        # response_serializer.is_valid(raise_exception=True)

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )



@extend_schema(request=GenerateAPIKeySerializer)
class RegenerateAPIKeyAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GenerateAPIKeySerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        contract = get_object_or_404(
            ContractModel,
            pk=serializer.validated_data["contract_id"],
            user=request.user,
        )

        raw_key = RegenerateAPIKeyService(
            actor=request.user,
            contract=contract,
        ).execute()

        response_serializer = APIKeySerializer(
            instance={"api_key": raw_key}
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK,
        )


class RevokeAPIKeyAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, api_key_id):
        api_key = get_object_or_404(
            APIKeyModel.objects.select_related("contract"),
            pk=api_key_id,
        )

        revoked_key = RevokeAPIKeyService(
            actor=request.user,
            api_key=api_key,
        ).execute()

        serializer = APIKeyStatusSerializer(revoked_key)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


@extend_schema(request=ParameterCreateSerializer)
class ParameterCreateAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ParameterCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        parameter = CreateParameterService(
            actor=request.user,
            validated_data=serializer.validated_data,
        ).execute()

        return Response(
            ParameterCreateSerializer(parameter).data,
            status=status.HTTP_201_CREATED,
        )


class ParameterListAPIView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ParameterSerializer

    def get_queryset(self):
        return ParameterQueryService(
            actor=self.request.user
        ).get_queryset()


class ParameterDetailAPIView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ParameterSerializer
    lookup_field = "id"

    def get_object(self):
        service = ParameterQueryService(actor=self.request.user)
        parameter = service.get_parameter(self.kwargs["id"])

        return get_object_or_404(
            service.get_queryset(),
            id=parameter.id if parameter else None,
        )


@extend_schema(request=AssignParameterSerializer)
class AssignParameterAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, contract_id):
        serializer = AssignParameterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        assignment = AssignParameterService(
            actor=request.user,
            contract_id=contract_id,
            parameter_id=serializer.validated_data["parameter_id"],
        ).execute()

        return Response(
            {
                "id": assignment.id,
                "contract_id": assignment.contract_id,
                "parameter_id": assignment.parameter_id,
                "assigned_by": assignment.assigned_by_id,
                "assigned_at": assignment.assigned_at,
            },
            status=status.HTTP_201_CREATED,
        )


class RevokeParameterAssignmentAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, contract_id, parameter_id):
        RevokeParameterAssignmentService(
            actor=request.user,
            contract_id=contract_id,
            parameter_id=parameter_id,
        ).execute()

        return Response(status=204)



@extend_schema(request=ParameterStatusSerializer)
class ParameterStatusAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, parameter_id):
        serializer = ParameterStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        parameter = ChangeParameterStatusService(
            actor=request.user,
            parameter_id=parameter_id,
            is_active=serializer.validated_data["is_active"],
        ).execute()

        return Response(
            ParameterSerializer(parameter).data,
            status=status.HTTP_200_OK,
        )