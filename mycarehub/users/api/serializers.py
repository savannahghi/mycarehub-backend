from django import forms
from django.contrib.auth import get_user_model
from drf_braces.serializers.form_serializer import FormSerializer, make_form_serializer_field
from rest_framework import serializers

from mycarehub.common.serializers import OrganisationSerializer, ProgramSerializer
from mycarehub.users.forms import UserRegistrationForm

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    organisation = OrganisationSerializer()
    program = ProgramSerializer()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "name",
            "gender",
            "date_of_birth",
            "user_type",
            "program",
            "organisation",
        ]


class UserRegistrationSerializer(FormSerializer):
    class Meta:
        form = UserRegistrationForm
        field_mapping = {
            forms.UUIDField: make_form_serializer_field(serializers.UUIDField),
        }
