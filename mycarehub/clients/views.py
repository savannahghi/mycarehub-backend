from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from mycarehub.common.models import Organisation, Program

from .models import Client
from .serializers import ClientSerializer


class ClientAPIView(APIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def get(self, request):
        users = Client.objects.all()
        serializer = ClientSerializer(users, many=True)

        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                data = serializer.validated_data

                # get organisation
                organisation = Organisation.objects.get(id=data["organisation_id"])

                # get program
                program = Program.objects.get(id=data["program_id"])

                new_user, _ = Client.objects.get_or_create(
                    id=data["client_id"],
                    defaults={
                        "name": data["name"],
                        "gender": data["gender"],
                        "date_of_birth": data["date_of_birth"],
                        "organisation": organisation,
                        "program": program,
                    },
                )

                # return the newly created client
                serialized_client = ClientSerializer(new_user)
                return Response(serialized_client.data, status=status.HTTP_201_CREATED)
            except Exception as e:  # noqa # pragma: nocover
                return Response(
                    {"exception": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )  # pragma: nocover

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            user = Client.objects.get(pk=pk)

            with transaction.atomic():
                user.delete()

        except Exception as e:  # pragma: nocover
            return Response(
                {"exception": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )  # pragma: nocover

        return Response(status=status.HTTP_204_NO_CONTENT)
