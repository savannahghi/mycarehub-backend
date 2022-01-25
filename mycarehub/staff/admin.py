from django.contrib import admin

from mycarehub.common.admin import BaseAdmin

from .models import Staff


@admin.register(Staff)
class StaffAdmin(BaseAdmin):
    pass
