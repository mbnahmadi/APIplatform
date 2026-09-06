# from django.shortcuts import render
# from .models import UserModel, ClientProfileModel, APITokenModel
# from .serializers import ClientProfileSerializer, LogoutSerializer, GenerateApiKeyResponseSerializer
# from .permissions import IsAdminUser
# from .service.api_token import GenerateApiKeyService

# from rest_framework import status, generics
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated

# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

# from drf_spectacular.utils import extend_schema
# # Create your views here.

# @extend_schema(request=LogoutSerializer)
# class LogoutAPIView(APIView):
#     def post(self, request):
#         serializer = LogoutSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         refresh_token  = serializer.validated_data["refresh"]
        
#         try:
#             # the library can decode and validate that specific token
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#             return Response(status=status.HTTP_205_RESET_CONTENT)
#         except (InvalidToken, TokenError) as e:
#             return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)


# class UserCreateView(generics.CreateAPIView):
#     queryset = ClientProfileModel.objects.all()
#     serializer_class = ClientProfileSerializer
#     permission_classes = [IsAdminUser]

# class UserRetreiveView(generics.ListAPIView):
#     queryset = ClientProfileModel.objects.all()
#     serializer_class = ClientProfileSerializer
#     permission_classes = [IsAdminUser]


# class UserRetreiveUpdateView(generics.RetrieveUpdateAPIView):
#     queryset = ClientProfileModel.objects.all()
#     serializer_class = ClientProfileSerializer
#     permission_classes = [IsAdminUser]


# class UserDeleteView(generics.DestroyAPIView):
#     queryset = ClientProfileModel.objects.all()
#     serializer_class = ClientProfileSerializer
#     permission_classes = [IsAdminUser]

#     def perform_destroy(self, instance):
#         user = getattr(instance, "user", None)
#         instance.delete()
#         if user:
#             user.delete()

# # ================ client ================
# class ClientProfileView(generics.RetrieveAPIView):
#     serializer_class = ClientProfileSerializer
#     # def get_queryset(self):
#     #     return ClientProfileModel.objects.filter(user=self.request.user)
#     def get_object(self):
#         return generics.get_object_or_404(ClientProfileModel, user=self.request.user)


# # ============= API token =======================
# class GenerateAPIToken(APIView):
#     def post(self, request):
#         key = GenerateApiKeyService(user=request.user)
#         api_key = key.execute()

#         serializer = GenerateApiKeyResponseSerializer({"api_key": api_key})
#         # if serializer.is_valid():
#         return Response(serializer.data)
#         # return Response({"error": "bad request"})