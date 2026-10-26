from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken


class LogoutService:
    def __init__(self, refresh_token):
        self.refresh_token = refresh_token

    def execute(self):
        try:
            token = RefreshToken(self.refresh_token)
            token.blacklist()
        except TokenError:
            raise ValidationError({
                "refresh": "Invalid or expired refresh token."
            })

        return {"detail": "Successfully logged out."}