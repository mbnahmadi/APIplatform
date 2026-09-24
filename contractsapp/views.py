from django.shortcuts import render
from django.shortcuts import render
# from .models import 
from .serializers import (
    ContractCreateSerializer,
    ContractSerializer,
    ContractUpdateSerializer,
    ContractStatusSerializer,
    ContractRenewSerializer,
    ContractHistorySerializer
    )

from .models import ContractModel, ContractHistoryModel
from .permissions import CanViewContracts, CanViewContractHistory
from .service.create_contract import CreateContractService
from .service.update_contract import UpdateContractService
from .service.contract_status import ChangeContractStatusService
from .service.contract_renewal import RenewContractService

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from rest_framework_simplejwt.authentication import JWTAuthentication


from drf_spectacular.utils import extend_schema
# Create your views here.

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