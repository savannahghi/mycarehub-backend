"""Common serializers."""
import logging
import uuid

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
    id = serializers.UUIDField(read_only=False, default=uuid.uuid4)

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
    organisation_id = serializers.UUIDField(write_only=True)

    class Meta(BaseSerializer.Meta):
        model = Organisation
        fields = ["id", "name", "code", "organisation_id", "phone_number", "email"]


class ProgramSerializer(BaseSerializer):
    organisation_id = serializers.UUIDField(write_only=True)
    program_id = serializers.UUIDField(write_only=True)

    class Meta(BaseSerializer.Meta):
        model = Program
        fields = ["id", "name", "facilities", "organisation_id", "program_id"]

    def update(self, instance, validated_data):
        facilities = validated_data.pop("facilities", None)
        if facilities:
            instance.facilities.clear()

            for facility in facilities:
                instance.facilities.add(facility)

        return super().update(instance, validated_data)
