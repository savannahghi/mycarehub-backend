from django import forms
from drf_braces.serializers.form_serializer import FormSerializer, make_form_serializer_field
from rest_framework import serializers

from mycarehub.common.serializers import OrganisationSerializer, ProgramSerializer

from .forms import ClientRegistrationForm
from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    organisation = OrganisationSerializer()
    program = ProgramSerializer()

    class Meta:
        model = Client
        fields = [
            "id",
            "name",
            "gender",
            "date_of_birth",
            "program",
            "organisation",
        ]


class ClientRegistrationSerializer(FormSerializer):
    class Meta:
        form = ClientRegistrationForm
        field_mapping = {
            forms.UUIDField: make_form_serializer_field(serializers.UUIDField),
        }
