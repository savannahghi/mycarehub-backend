"""Common serializers."""
import logging

from django.contrib.auth import get_user_model
from rest_framework import serializers

from mycarehub.common.models import Organisation, Program

from ..models import Facility, UserFacilityAllotment
from .base_serializers import BaseSerializer

LOGGER = logging.getLogger(__name__)

User = get_user_model()


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "name",
        ]


class FacilitySerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Facility
        fields = "__all__"


class UserFacilityAllotmentSerializer(BaseSerializer):

    user_data = SimpleUserSerializer(source="user", read_only=True)
    user_name = serializers.ReadOnlyField(source="user.__str__")
    allotment_type_name = serializers.ReadOnlyField(source="get_allotment_type_display")

    class Meta(BaseSerializer.Meta):
        model = UserFacilityAllotment
        fields = "__all__"


class OrganisationSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Organisation
        fields = ["id", "organisation_name", "code"]


class ProgramSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Program
        fields = ["id", "name"]
