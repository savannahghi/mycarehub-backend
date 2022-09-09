from django import forms
from drf_braces.serializers.form_serializer import FormSerializer, make_form_serializer_field
from phonenumber_field.formfields import PhoneNumberField
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer, UUIDField

from mycarehub.staff.models import Staff

from .forms import StaffRegistrationForm


class StaffRegistrationSerializer(FormSerializer):
    class Meta:
        form = StaffRegistrationForm
        fields = "__all__"
        field_mapping = {
            PhoneNumberField: make_form_serializer_field(CharField),
            forms.UUIDField: make_form_serializer_field(UUIDField),
        }


class StaffSerializer(ModelSerializer):
    class Meta:
        model = Staff
        fields = "__all__"
