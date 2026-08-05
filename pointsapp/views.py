import csv
import io

from django.shortcuts import render
from .models import UploadFileModel, UserPointModel
from .serializers import UploadFileSerializer, PointSerializer
from .tasks import process_csv_file_task
from usersapp.permissions import IsAdminUser
from usersapp.api_key_authenticate import APIKeyAuthentication

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.parsers import MultiPartParser, FormParser
# Create your views here.



class DocumentListCreateView(generics.CreateAPIView):
    queryset = UploadFileModel.objects.all()
    serializer_class = UploadFileSerializer
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        upload = serializer.save(uploaded_by=self.request.user)

        process_csv_file_task.delay(upload.id)


class PointListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    # queryset = UserPointModel.objects.all()
    serializer_class = PointSerializer
    def get_queryset(self):
        user_id = self.kwargs.get("user")
        return UserPointModel.objects.filter(owner=user_id)


class PointCreateView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = UserPointModel.objects.all()
    serializer_class = PointSerializer

    def perform_create(self, serializer):
        user_id = self.kwargs.get("user")
        serializer.save(owner_id=user_id)


class PointdeleteView(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]
    # queryset = UserPointModel.objects.all()
    serializer_class = PointSerializer

    def get_queryset(self):
        user_id = self.kwargs.get("user")
        return UserPointModel.objects.filter(owner=user_id)


class PointRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAdminUser]
    # queryset = UserPointModel.objects.all()
    serializer_class = PointSerializer

    def get_queryset(self):
            user_id = self.kwargs.get("user")
            return UserPointModel.objects.filter(owner=user_id)


# =============== client ===============
class ClientPointView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = PointSerializer
    def get_queryset(self):
        return UserPointModel.objects.filter(owner=self.request.user)



class WeatherTestView(APIView):
    authentication_classes = [APIKeyAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "message": "You are authenticated",
            "user": request.user.username,
        })