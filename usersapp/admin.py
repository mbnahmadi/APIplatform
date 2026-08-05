from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserModel, ClientProfileModel, APITokenModel

# Register your models here.

# admin.site.register(UserModel, UserAdmin)
admin.site.register(ClientProfileModel)
admin.site.register(APITokenModel)

@admin.register(UserModel)
class UserModelAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('role',)

    fieldsets = UserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )