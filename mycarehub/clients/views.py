from rest_framework.viewsets import ModelViewSet

from mycarehub.clients.models import (
    Client,
    ClientFacility,
    Identifier,
    RelatedPerson,
    SecurityQuestion,
    SecurityQuestionResponse,
)
from mycarehub.clients.serializers import (
    ClientFacilitySerializer,
    ClientSerializer,
    IdentifierSerializer,
    RelatedPersonSerializer,
    SecurityQuestionResponseSerializer,
    SecurityQuestionSerializer,
)


class IdentifierViewSet(ModelViewSet):
    queryset = Identifier.objects.order_by("pk")
    serializer_class = IdentifierSerializer


class SecurityQuestionViewSet(ModelViewSet):
    queryset = SecurityQuestion.objects.order_by("pk")
    serializer_class = SecurityQuestionSerializer


class SecurityQuestionResponseViewSet(ModelViewSet):
    queryset = SecurityQuestionResponse.objects.order_by("pk")
    serializer_class = SecurityQuestionResponseSerializer


class RelatedPersonViewSet(ModelViewSet):
    queryset = RelatedPerson.objects.order_by("pk")
    serializer_class = RelatedPersonSerializer


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.order_by("pk")
    serializer_class = ClientSerializer


class ClientFacilityViewSet(ModelViewSet):
    queryset = ClientFacility.objects.order_by("pk")
    serializer_class = ClientFacilitySerializer
