from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from mycarehub.common.dashboard import get_mycarehub_facilities_queryset
from mycarehub.common.filters import FacilityFilter, UserFacilityAllotmentFilter
from mycarehub.common.models import Organisation, Program, UserFacilityAllotment
from mycarehub.common.serializers import (
    FacilitySerializer,
    OrganisationRegistrationSerializer,
    OrganisationSerializer,
    ProgramRegistrationSerializer,
    ProgramSerializer,
    UserFacilityAllotmentSerializer,
)

from ..base_views import BaseView


class FacilityViewSet(BaseView):
    queryset = get_mycarehub_facilities_queryset()
    serializer_class = FacilitySerializer
    filterset_class = FacilityFilter
    ordering_fields = ("name", "mfl_code", "county", "phone", "sub_county", "ward")
    search_fields = (
        "name",
        "mfl_code",
        "registration_number",
    )


class UserFacilityViewSet(BaseView):
    queryset = UserFacilityAllotment.objects.active().order_by(
        "user__name", "user__username", "-updated", "-created"
    )
    serializer_class = UserFacilityAllotmentSerializer
    filterset_class = UserFacilityAllotmentFilter
    ordering_fields = ("user__name", "user__username", "allotment_type")
    search_fields = ("allotment_type", "user__name", "user__username")


class OrganisationAPIView(APIView):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationRegistrationSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                validated_data = serializer.validated_data
                data = {
                    "id": validated_data["organisation_id"],
                    "organisation_name": validated_data["name"],
                    "code": validated_data["code"],
                    "phone_number": validated_data["phone_number"],
                    "email_address": validated_data["email"],
                }

                new_org = Organisation.objects.create(**data)

                serialized_org = OrganisationSerializer(new_org)

                return Response(status=status.HTTP_201_CREATED, data=serialized_org.data)
            except Exception as e:  # noqa # pragma: nocover
                return Response(
                    {"exception": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )  # pragma: nocover

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProgramAPIView(APIView):
    queryset = Program.objects.all()
    serializer_class = ProgramRegistrationSerializer

    def get(self, request):
        programs = Program.objects.all()
        serializer = ProgramSerializer(programs, many=True)

        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                validated_data = serializer.validated_data
                data = {"id": validated_data["program_id"], "name": validated_data["name"]}

                org = Organisation.objects.get(id=validated_data["organisation_id"])
                data["organisation"] = org

                new_program = Program.objects.create(**data)

                serialized_program = ProgramSerializer(new_program)

                return Response(status=status.HTTP_201_CREATED, data=serialized_program.data)
            except Exception as e:  # noqa # pragma: nocover
                return Response(
                    {"exception": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )  # pragma: nocover

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        program = get_object_or_404(Program, pk=pk)

        data = request.data
        serializer = ProgramSerializer(
            instance=program, context={"request": request}, data=data, partial=True
        )
        if serializer.is_valid():
            updated_program = serializer.save()
            return Response(
                status=status.HTTP_200_OK, data=ProgramSerializer(updated_program).data
            )

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
