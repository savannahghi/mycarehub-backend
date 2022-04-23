from rest_framework.serializers import (
    BooleanField,
    CharField,
    ChoiceField,
    DateField,
    ModelSerializer,
    MultipleChoiceField,
    Serializer,
)

from mycarehub.clients.models import (
    Caregiver,
    Client,
    ClientFacility,
    HealthDiaryAttachment,
    Identifier,
    RelatedPerson,
    SecurityQuestion,
    SecurityQuestionResponse,
)
from mycarehub.users.models import GenderChoices

from .forms import get_client_types, get_facility_choices, validate_date_past


class IdentifierSerializer(ModelSerializer):
    class Meta:
        model = Identifier
        fields = "__all__"


class SecurityQuestionSerializer(ModelSerializer):
    class Meta:
        model = SecurityQuestion
        fields = "__all__"


class SecurityQuestionResponseSerializer(ModelSerializer):
    class Meta:
        model = SecurityQuestionResponse
        fields = "__all__"


class RelatedPersonSerializer(ModelSerializer):
    class Meta:
        model = RelatedPerson
        fields = "__all__"


class CaregiverSerializer(ModelSerializer):
    class Meta:
        model = Caregiver
        fields = "__all__"


class ClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class ClientFacilitySerializer(ModelSerializer):
    class Meta:
        model = ClientFacility
        fields = "__all__"


class ClientRegistrationSerializer(Serializer):
    facility = ChoiceField(
        required=True,
        choices=get_facility_choices(),
        label="Client's Facility/Clinic",
        help_text="The client's currently assigned facility/clinic",
    )

    client_types = MultipleChoiceField(
        required=False,
        choices=get_client_types(),
        label="Client Type e.g PMTCT",
        help_text="The client's current care classification",
    )

    name = CharField(
        required=True,
        max_length=255,
        label="Name",
        help_text="The client's full name i.e family, given and other names, on one row",
    )

    gender = ChoiceField(
        required=True,
        choices=GenderChoices,
        label="Gender",
        help_text="Pick the client's gender from the drop-down list",
    )

    date_of_birth = DateField(
        required=True,
        label="Date of birth",
        help_text="Select the client's date of birth",
        validators=[
            validate_date_past,
        ],
    )

    phone_number = CharField(
        required=True,
        label="Phone Number",
        help_text="The client's phone number",
    )

    enrollment_date = DateField(
        required=True,
        label="Enrollment date",
        help_text="When the client was first enrolled in care",
        validators=[
            validate_date_past,
        ],
    )

    ccc_number = CharField(
        required=True,
        label="CCC Number",
        help_text="Comprehensive Care Clinic Number, to be used as the primary identifier",
    )

    counselled = BooleanField(
        required=False,
        label="Client Counselled?",
        help_text="Whether the client has been counselled",
    )

    class Meta:
        fields = "__all__"


class HealthDiaryAttachmentSerializer(ModelSerializer):
    class Meta:
        model = HealthDiaryAttachment
        fields = "__all__"
