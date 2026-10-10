from rest_framework.exceptions import NotFound

from ..models import ContractPointModel


class CheckPointAccessService:
    def __init__(self, api_key, point_id):
        self.api_key = api_key
        self.point_id = point_id

    def execute(self):
        contract = self.api_key.contract

        assignment_exists = ContractPointModel.objects.filter(
            contract=contract,
            point_id=self.point_id,
            revoked_at__isnull=True,
        ).exists()

        if not assignment_exists:
            raise NotFound(
                "Point not found or not assigned to this contract."
            )

        return True