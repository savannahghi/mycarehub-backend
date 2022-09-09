from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from mycarehub.clients.models import Caregiver, Client, ClientFacility
from mycarehub.clients.serializers import (
    CaregiverSerializer,
    ClientFacilitySerializer,
    ClientRegistrationSerializer,
    ClientSerializer,
)
from mycarehub.common.models.common_models import Facility
from mycarehub.users.models import User


class CaregiverViewSet(ModelViewSet):
    queryset = Caregiver.objects.order_by("pk")
    serializer_class = CaregiverSerializer


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.order_by("pk")
    serializer_class = ClientSerializer


class ClientFacilityViewSet(ModelViewSet):
    queryset = ClientFacility.objects.order_by("pk")
    serializer_class = ClientFacilitySerializer


class ClientRegistrationView(APIView):
    queryset = Client.objects.all()  # to enable model permissions
    serializer_class = ClientRegistrationSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                data = serializer.validated_data
                request_user = request.user
                org = request_user.organisation
                flavour = "CONSUMER"
                with transaction.atomic():
                    # TODO: use organisation unique identifier when workflow is set up
                    # org = Organisation.objects.get(id=data["organisation_id"])

                    new_user, _ = User.objects.get_or_create(
                        id=data["user_id"],
                        defaults={
                            "name": data["name"],
                            "username": data["handle"],
                            "gender": data["gender"],
                            "date_of_birth": data["date_of_birth"],
                            "user_type": "CLIENT",
                            "phone": data["phone_number"],
                            "flavour": flavour,
                            "organisation": org,
                        },
                    )

                    # retrieve the facility by the unique name
                    # TODO: use facility unique identifier when workflow is set up
                    facility_name = data["facility_name"]
                    facility = Facility.objects.get(name=facility_name)

                    # create a client
                    client, _ = Client.objects.get_or_create(
                        user=new_user,
                        defaults={
                            "id": data["client_id"],
                            "client_types": list(data["client_types"]),
                            "user": new_user,
                            "enrollment_date": data["enrollment_date"],
                            "current_facility": facility,
                            "organisation": org,
                            "created_by": request_user.pk,
                            "updated_by": request_user.pk,
                        },
                    )

                    ClientFacility.objects.get_or_create(
                        client=client,
                        facility=facility,
                        defaults={
                            "organisation": org,
                            "created_by": request_user.pk,
                            "updated_by": request_user.pk,
                        },
                    )

                    # return the newly created client
                    serialized_client = ClientSerializer(client)
                return Response(serialized_client.data, status=status.HTTP_201_CREATED)
            except Exception as e:  # noqa # pragma: nocover
                return Response(
                    {"exception": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )  # pragma: nocover
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            user = User.objects.get(pk=pk)
            client = Client.objects.get(user=user)
            allocation = ClientFacility.objects.get(client=client)

            with transaction.atomic():
                allocation.delete()
                client.delete()
                user.delete()

        except Exception as e:
            return Response(
                {"exception": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_200_OK)
