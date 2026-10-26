from usersapp.authentication import VersionedJWTAuthentication

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
# from rest_framework_simplejwt.authentication import VersionedJWTAuthentication

from .serializers import (
    PointCreateSerializer,
    PointSerializer,
    AssignPointSerializer
)
from .service.create_point import CreatePointService
from .service.point_query import PointQueryService
from .service.assign_point import AssignPointService
from .service.revoke_point_assignment import RevokePointAssignmentService

from django.shortcuts import get_object_or_404
from rest_framework import generics

from drf_spectacular.utils import extend_schema


@extend_schema(request=PointCreateSerializer)
class PointCreateAPIView(APIView):
    authentication_classes = [VersionedJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PointCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        point = CreatePointService(
            actor=request.user,
            validated_data=serializer.validated_data,
        ).execute()

        return Response(
            PointCreateSerializer(point).data,
            status=status.HTTP_201_CREATED,
        )



class PointListAPIView(generics.ListAPIView):
    authentication_classes = [VersionedJWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PointSerializer

    def get_queryset(self):
        service = PointQueryService(actor=self.request.user)
        return service.get_queryset()


class PointDetailAPIView(generics.RetrieveAPIView):
    authentication_classes = [VersionedJWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PointSerializer
    lookup_field = "id"

    def get_object(self):
        service = PointQueryService(actor=self.request.user)
        point = service.get_point(point_id=self.kwargs["id"])

        return get_object_or_404(
            service.get_queryset(),
            id=point.id if point else None,
        )    


@extend_schema(request=AssignPointSerializer)
class AssignPointAPIView(APIView):
    authentication_classes = [VersionedJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, contract_id):
        serializer = AssignPointSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        assignment = AssignPointService(
            actor=request.user,
            contract_id=contract_id,
            point_id=serializer.validated_data["point_id"],
        ).execute()

        return Response(
            {
                "id": assignment.id,
                "contract_id": assignment.contract_id,
                "point_id": assignment.point_id,
                "assigned_by": assignment.assigned_by_id,
                "assigned_at": assignment.assigned_at,
            },
            status=status.HTTP_201_CREATED,
        )



class RemovePointAPIView(APIView):
    authentication_classes = [VersionedJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, contract_id, point_id):
        RevokePointAssignmentService(
            actor=request.user,
            contract_id=contract_id,
            point_id=point_id,
        ).execute()

        return Response(status=204)