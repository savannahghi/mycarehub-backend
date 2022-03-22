from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from mycarehub.authority.models import AuthorityRole
from mycarehub.clients.models import Identifier
from mycarehub.common.models.common_models import Contact, Facility
from mycarehub.users.models import User

from .models import Staff
from .serializers import StaffRegistrationSerializer, StaffSerializer


class StaffRegistrationView(APIView):
    queryset = Staff.objects.all()
    serializer_class = StaffRegistrationSerializer

    @transaction.atomic
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                data = serializer.validated_data
                request_user = request.user
                org = request_user.organisation
                flavour = "PRO"

                new_user, _ = User.objects.get_or_create(
                    username=data["name"],
                    defaults={
                        "name": data["name"],
                        "gender": data["gender"],
                        "date_of_birth": data["date_of_birth"],
                        "user_type": "STAFF",
                        "phone": data["phone_number"],
                        "flavour": flavour,
                        "organisation": org,
                    },
                )

                # create a contact, already opted in
                contact_data = {
                    "contact_value": data["phone_number"],  # noqa
                    "flavour": flavour,
                    "contact_type": "PHONE",
                    "opted_in": True,
                    "flavour": flavour,
                    "user": new_user,
                    "organisation": org,
                    "created_by": request_user.pk,
                    "updated_by": request_user.pk,
                }
                contact = Contact.objects.create(**contact_data)

                # create an identifier (ID)
                identifier, _ = Identifier.objects.get_or_create(
                    identifier_value=data["id_number"],
                    identifier_type="NATIONAL_ID",
                    defaults={
                        "identifier_use": "OFFICIAL",
                        "description": "ID Number, Primary Identifier",
                        "is_primary_identifier": True,
                        "organisation": org,
                        "created_by": request_user.pk,
                        "updated_by": request_user.pk,
                    },
                )

                # retrieve the facility by the unique name
                facility_name = data["facility"]
                facility = Facility.objects.get(name=facility_name)

                # create a staff
                staff, _ = Staff.objects.get_or_create(
                    user=new_user,
                    defaults={
                        "user": new_user,
                        "default_facility": facility,
                        "staff_number": data["staff_number"],
                        "organisation": org,
                        "created_by": request_user.pk,
                        "updated_by": request_user.pk,
                    },
                )

                # add the contact to the staff
                staff.contacts.add(contact)

                # add facility to the staff
                staff.facilities.add(facility)

                # add the identifier to the staff
                staff.identifiers.add(identifier)

                # add user to roles
                for role in AuthorityRole.objects.filter(name=data["role"]):
                    role.users.add(new_user)
                # return the newly created staff
                serialized_staff = StaffSerializer(staff)
                return Response(serialized_staff.data, status=status.HTTP_201_CREATED)
            except Exception as e:  # noqa # pragma: nocover
                return Response(
                    {"exception": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )  # pragma: nocover
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
