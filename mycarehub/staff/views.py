from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from mycarehub.common.models.common_models import Facility
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
                            "user_type": "STAFF",
                            "phone": data["phone_number"],
                            "flavour": flavour,
                            "organisation": org,
                        },
                    )
                    # retrieve the facility by the unique name
                    # TODO: use facility unique identifier when workflow is set up
                    facility_name = data["facility_name"]
                    facility = Facility.objects.get(name=facility_name)

                    # create a staff
                    staff, _ = Staff.objects.get_or_create(
                        user=new_user,
                        defaults={
                            "id": data["staff_id"],
                            "user": new_user,
                            "default_facility": facility,
                            "staff_number": data["staff_number"],
                            "organisation": org,
                            "created_by": request_user.pk,
                            "updated_by": request_user.pk,
                        },
                    )

                    # add facility to the staff
                    staff.facilities.add(facility)

                # return the newly created staff
                serialized_staff = StaffSerializer(staff)
                return Response(serialized_staff.data, status=status.HTTP_201_CREATED)
            except Exception as e:  # noqa # pragma: nocover
                return Response(
                    {"exception": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )  # pragma: nocover
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            user = User.objects.get(pk=pk)
            staff = Staff.objects.get(user=user)

            with transaction.atomic():
                staff.facilities.clear()
                staff.delete()
                user.delete()

        except Exception as e:
            return Response(
                {"exception": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_200_OK)
