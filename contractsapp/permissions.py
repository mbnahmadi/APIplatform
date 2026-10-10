from rest_framework.permissions import BasePermission


class CanViewContracts(BasePermission):

    def has_permission(self, request, view):
        return request.user.has_perm(
            "contractsapp.view_contract"
        )


class CanViewContractHistory(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm(
            "contractsapp.view_contract_history"
        )