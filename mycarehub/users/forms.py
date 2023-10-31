from datetime import date

from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

User = get_user_model()


def validate_date_past(value):
    if not isinstance(value, date):
        raise ValidationError(
            _("%(value)s is not a date"),
            params={"value": value},
        )

    if value > timezone.now().date():
        raise ValidationError(
            _("%(value)s is a date that is in the future"),
            params={"value": value},
        )


class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(admin_forms.UserCreationForm):
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

        error_messages = {"username": {"unique": _("This username has already been taken.")}}
