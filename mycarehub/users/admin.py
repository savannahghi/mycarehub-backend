from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from mycarehub.common.admin import BaseAdmin
from mycarehub.users.forms import UserChangeForm, UserCreationForm

from .models import Metric

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("name", "email", "gender")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["username", "name", "is_superuser", "permissions", "gps"]
    search_fields = ["name"]


@admin.register(Metric)
class MetricAdmin(BaseAdmin):
    list_display = [
        "user",
        "timestamp",
        "metric_type",
    ]
