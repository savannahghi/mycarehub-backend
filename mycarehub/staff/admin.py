from django.contrib import admin

from mycarehub.common.admin import BaseAdmin

from .models import ServiceRequest, Staff


@admin.register(Staff)
class StaffAdmin(BaseAdmin):
    pass


@admin.register(ServiceRequest)
class ServiceRequestAdmin(BaseAdmin):
    pass
