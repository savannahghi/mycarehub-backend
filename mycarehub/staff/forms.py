from django import forms
from phonenumber_field.formfields import PhoneNumberField

from mycarehub.clients.forms import get_facility_choices, validate_date_past
from mycarehub.users.models import GenderChoices


class StaffRegistrationForm(forms.Form):
    """
    This form is used in a HTML UI and via a Django REST Framework serializer
    to register new Staffs.
    """

    user_id = forms.UUIDField(
        required=True, label="User ID", help_text="The staff's unique user identifier"
    )

    name = forms.CharField(
        required=True,
        max_length=255,
        label="Name",
        help_text="The Staff's full name i.e family, given and other names, on one row",
    )

    handle = forms.CharField(
        required=True,
        max_length=255,
        label="Username",
        help_text="The staff's unique username",
    )

    gender = forms.ChoiceField(
        required=True,
        choices=GenderChoices.choices,
        label="Gender",
        help_text="Pick the Staff's gender from the drop-down list",
    )

    date_of_birth = forms.DateField(
        required=True,
        label="Date of birth",
        help_text="Select the Staff's date of birth",
        validators=[
            validate_date_past,
        ],
    )

    phone_number = PhoneNumberField(
        required=True,
        label="Phone Number",
        help_text="The Staff's phone number",
    )

    organisation_id = forms.UUIDField(
        required=True,
        label="Organisation ID",
        help_text="The staff's currently assigned facility/clinic",
    )

    facility_id = forms.UUIDField(
        required=True,
        label="Staff's Facility/Clinic ID",
        help_text="The staff's currently assigned facility/clinic",
    )

    facility_name = forms.ChoiceField(
        required=True,
        choices=get_facility_choices,
        label="Staff's Facility/Clinic",
        help_text="The staff's currently assigned facility/clinic",
    )

    staff_id = forms.UUIDField(
        required=True, label="Staff ID", help_text="The staff's unique user identifier"
    )

    staff_number = forms.CharField(
        required=True,
        label="Staff Number",
        help_text="The Staff's currently assigned staff number",
    )
