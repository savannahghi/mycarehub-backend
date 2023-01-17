from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from mycarehub.common.models import Organisation, Program

from .serializers import UserRegistrationSerializer, UserSerializer

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class UserAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)

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

                new_user, _ = User.objects.get_or_create(
                    id=data["user_id"],
                    defaults={
                        "name": data["name"],
                        "username": data["username"],
                        "gender": data["gender"],
                        "date_of_birth": data["date_of_birth"],
                        "user_type": data["user_type"],
                        "organisation": organisation,
                        "program": program,
                    },
                )

                serialized_user = UserSerializer(new_user)
                return Response(serialized_user.data, status=status.HTTP_201_CREATED)
            except Exception as e:  # noqa # pragma: nocover
                return Response(
                    {"exception": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )  # pragma: nocover

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            user = User.objects.get(pk=pk)

            with transaction.atomic():
                user.delete()

        except Exception as e:  # pragma: nocover
            return Response(
                {"exception": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )  # pragma: nocover

        return Response(status=status.HTTP_204_NO_CONTENT)
