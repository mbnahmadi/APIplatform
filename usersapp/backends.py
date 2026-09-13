from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.backends import ModelBackend

User = get_user_model()


class EmailOrUsernameBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        identifier = kwargs.get("identifier") or username

        if not identifier or not password:
            return None

        user = User.objects.filter(
            email__iexact=identifier,
        ).first()

        if user is None:
            user = User.objects.filter(
                username__iexact=identifier,
            ).first()

        if user is None:
            return None

        if not user.check_password(password):
            return None

        if not user.is_active:
            return None

        return user

    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None