from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.

# admin.site.register(UserModel, UserAdmin)
# admin.site.register(ClientProfileModel)
# admin.site.register(APITokenModel)

@admin.register(User)
class UserModelAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('role',)

    fieldsets = UserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )