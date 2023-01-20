from django import forms

from mycarehub.users.forms import validate_date_past
from mycarehub.users.models import GenderChoices


class ClientRegistrationForm(forms.Form):
    client_id = forms.UUIDField(
        required=True, label="Client ID", help_text="The client's unique user identifier"
    )

    name = forms.CharField(
        required=True,
        max_length=255,
        label="Name",
        help_text="The client's full name i.e family, given and other names, on one row",
    )

    gender = forms.ChoiceField(
        required=True,
        choices=GenderChoices.choices,
        label="Gender",
        help_text="Pick the client's gender from the drop-down list",
    )

    date_of_birth = forms.DateField(
        required=True,
        label="Date of birth",
        help_text="Select the client's date of birth",
        validators=[
            validate_date_past,
        ],
    )

    organisation_id = forms.UUIDField(
        required=True,
        label="Organisation ID",
        help_text="The client's currently assigned organisation",
    )

    program_id = forms.UUIDField(
        required=True,
        label="Program ID",
        help_text="The client's currently assigned program",
    )
