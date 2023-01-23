from django.contrib import admin

from mycarehub.common.admin import BaseAdmin

from .models import Client


@admin.register(Client)
class ClientAdmin(BaseAdmin):
    pass
