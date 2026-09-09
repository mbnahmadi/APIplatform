from django.contrib import admin
from .models import ContractModel, ContractHistoryModel, ParameterModel,  APIKeyModel
# Register your models here.


admin.site.register(ContractModel)
admin.site.register(ContractHistoryModel)
admin.site.register(ParameterModel)
admin.site.register(APIKeyModel)
