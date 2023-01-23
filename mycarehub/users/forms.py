from datetime import date

from django import forms
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from mycarehub.users.models import GenderChoices, UserTypes

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


class UserRegistrationForm(forms.Form):
    user_id = forms.UUIDField(
        required=True, label="User ID", help_text="The user's unique user identifier"
    )

    name = forms.CharField(
        required=True,
        max_length=255,
        label="Name",
        help_text="The user's full name i.e family, given and other names, on one row",
    )

    username = forms.CharField(
        required=True,
        max_length=255,
        label="Username",
        help_text="The user's unique username",
    )

    gender = forms.ChoiceField(
        required=True,
        choices=GenderChoices.choices,
        label="Gender",
        help_text="Pick the user's gender from the drop-down list",
    )

    date_of_birth = forms.DateField(
        required=True,
        label="Date of birth",
        help_text="Select the user's date of birth",
        validators=[
            validate_date_past,
        ],
    )

    user_type = forms.ChoiceField(
        required=True,
        choices=UserTypes.choices,
        label="User Type",
        help_text="Pick the user's user type from the drop-down list",
    )

    organisation_id = forms.UUIDField(
        required=True,
        label="Organisation ID",
        help_text="The user's currently assigned organisation",
    )

    program_id = forms.UUIDField(
        required=True,
        label="Program ID",
        help_text="The user's currently assigned program",
    )
