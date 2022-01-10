from rest_framework.serializers import ModelSerializer

from mycarehub.clients.models import (
    Caregiver,
    Client,
    ClientFacility,
    Identifier,
    RelatedPerson,
    SecurityQuestion,
    SecurityQuestionResponse,
)


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
