import csv
import io

from django.shortcuts import render
from .models import UploadFileModel, UserPointModel
from .serializers import UploadFileSerializer
from usersapp.permissions import IsAdminUser
from .tasks import process_csv_file_task

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.parsers import MultiPartParser, FormParser
# Create your views here.



class DocumentListCreateView(generics.CreateAPIView):
    queryset = UploadFileModel.objects.all()
    serializer_class = UploadFileSerializer
    # permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        upload_instance = serializer.save(user=self.request.user)

        process_csv_file_task.delay(upload_instance.id, self.request.user.id)