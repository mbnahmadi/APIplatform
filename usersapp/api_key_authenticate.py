# from rest_framework.authentication import BaseAuthentication
# from rest_framework.exceptions import AuthenticationFailed
# from .models import APITokenModel

# from django.conf import settings

# class APIKeyAuthentication(BaseAuthentication):

#     def authenticate(self, request):
#         authorization = request.headers.get('Authorization')
#         if not authorization:
#             return None
#         parts = authorization.split()

#         if len(parts) != 2:
#             raise AuthenticationFailed(
#                 "Invalid Authorization header format."
#             )
        
#         if parts[0].lower() != settings.AUTHORIZATION_SCHEME.lower():
#             raise AuthenticationFailed(
#                 "Invalid authentication scheme."
#             )

#         if not parts[1].startswith(settings.API_KEY_PREFIX):
#             raise AuthenticationFailed(
#                 "Invalid Token"
#             )

#         api_key = parts[1]
#         token = APITokenModel.get_by_api_key(api_key)
#         if not token:
#             raise AuthenticationFailed("Invalid API Key")

#         if not token.is_active:
#             raise AuthenticationFailed("Token is not active")

#         if not token.user.is_active:
#             raise AuthenticationFailed("User is not active")

#         return (token.user, token)
            

        