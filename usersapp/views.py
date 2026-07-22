from django.shortcuts import render
from .models import UserModel, ClientProfileModel
from .serializsers import ClientProfileSerializer

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
# Create your views here.

class LogoutAPIView(APIView):
    def post(self, request):
        refresh_token  = request.data.get('refresh')
        if not refresh_token:
            return Response({"detail":"Refresh token required."}, status=status.HTTP_400_BAD_REQUEST)  
        
        try:
            # the library can decode and validate that specific token
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except (InvalidToken, TokenError) as e:
            return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)



class UserCreateView(generics.CreateAPIView):
    queryset = ClientProfileModel.objects.all()
    serializer_class = ClientProfileSerializer

class UserRetreiveView(generics.ListAPIView):
    queryset = ClientProfileModel.objects.all()
    serializer_class = ClientProfileSerializer

class UserRetreiveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = ClientProfileModel.objects.all()
    serializer_class = ClientProfileSerializer

class UserDeleteView(generics.DestroyAPIView):
    queryset = ClientProfileModel.objects.all()
    serializer_class = ClientProfileSerializer

    def perform_destroy(self, instance):
        user = getattr(instance, "user", None)
        instance.delete()
        if user:
            user.delete()