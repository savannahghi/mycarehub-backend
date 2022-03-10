from django.contrib import admin

from mycarehub.common.admin import BaseAdmin

from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(BaseAdmin):
    pass
