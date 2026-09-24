from ..models import ContractHistoryModel


class CreateContractHistoryService:
    def __init__(
        self,
        contract,
        changed_by,
        field_name,
        old_value,
        new_value,
    ):
        self.contract = contract
        self.changed_by = changed_by
        self.field_name = field_name
        self.old_value = old_value
        self.new_value = new_value

    def execute(self):
        return ContractHistoryModel.objects.create(
            contract=self.contract,
            changed_by=self.changed_by,
            field_name=self.field_name,
            old_value=str(self.old_value) if self.old_value is not None else None,
            new_value=str(self.new_value) if self.new_value is not None else None,
        )