from rest_framework import serializers

from mycarehub.common.serializers import OrganisationSerializer, ProgramSerializer

from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    organisation = OrganisationSerializer(read_only=True)
    program = ProgramSerializer(read_only=True)
    organisation_id = serializers.UUIDField(write_only=True)
    program_id = serializers.UUIDField(write_only=True)
    client_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Client
        fields = [
            "id",
            "name",
            "gender",
            "date_of_birth",
            "program",
            "organisation",
            "program_id",
            "organisation_id",
            "client_id",
        ]
