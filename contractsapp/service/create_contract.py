from ..models import ContractModel
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from rest_framework.exceptions import PermissionDenied

User = get_user_model()


class CreateContractService:

    def __init__(
        self,
        actor,
        user,
        start_date,
        end_date,
        request_quota,
        rate_limit,
    ):
        self.actor = actor
        self.user = user
        self.start_date = start_date
        self.end_date = end_date
        self.request_quota = request_quota
        self.rate_limit = rate_limit

    def execute(self):

        if not self.actor.has_perm(
            "contractsapp.create_contract"
        ):
            raise PermissionDenied(
                "You do not have permission to create contracts."
            )

        if self.user.role != User.Role.CLIENT:
            raise ValidationError(
                "Contract can only be created for a client."
            )

        contract = ContractModel.objects.create(
            user=self.user,
            start_date=self.start_date,
            end_date=self.end_date,
            request_quota=self.request_quota,
            rate_limit=self.rate_limit,
        )

        return contract