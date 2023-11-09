from django.contrib.auth import get_user_model
from rest_framework import serializers

from mycarehub.common.serializers import OrganisationSerializer, ProgramSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    organisation = OrganisationSerializer(read_only=True)
    program = ProgramSerializer(read_only=True)

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
