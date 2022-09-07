from django import forms
from drf_braces.serializers.form_serializer import FormSerializer, make_form_serializer_field
from phonenumber_field.formfields import PhoneNumberField
from rest_framework.serializers import CharField, ListField, ModelSerializer, UUIDField

from mycarehub.clients.models import Caregiver, Client, ClientFacility

from .forms import ClientRegistrationForm


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


class ClientRegistrationSerializer(FormSerializer):
    class Meta:
        form = ClientRegistrationForm
        fields = "__all__"
        field_mapping = {
            PhoneNumberField: make_form_serializer_field(CharField),
            forms.MultipleChoiceField: make_form_serializer_field(ListField),
            forms.UUIDField: make_form_serializer_field(UUIDField),
        }
