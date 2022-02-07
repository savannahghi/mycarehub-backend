from django.contrib import admin

from mycarehub.common.admin import BaseAdmin

from .models import AuthorityPermission, AuthorityRole


# Register your models here.
@admin.register(AuthorityPermission)
class AuthorityPermissionAdmin(BaseAdmin):
    pass


@admin.register(AuthorityRole)
class AuthorityRoleAdmin(BaseAdmin):
    pass
