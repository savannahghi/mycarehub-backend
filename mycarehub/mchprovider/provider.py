from allauth.socialaccount.adapter import get_adapter
from allauth.socialaccount.providers.base import ProviderAccount, ProviderException
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider
from django.core.exceptions import ObjectDoesNotExist

from mycarehub.common.models import Facility, Organisation, Program


class MycarehubAccount(ProviderAccount):
    pass


class MycarehubProvider(OAuth2Provider):
    id = "mycarehub"
    name = "Mycarehub"
    account_class = MycarehubAccount

    def __init__(self, request, app=None):
        if app is None:
            app = get_adapter().get_app(request, self.id)
        super().__init__(request, app=app)

    def get_default_scope(self):
        return []

    def extract_uid(self, data):
        return str(data["staff_id"])

    def extract_common_fields(self, data):
        organisation_id = data.get("organisation_id")
        try:
            Organisation.objects.get(pk=organisation_id)
        except ObjectDoesNotExist:
            raise ProviderException(
                """
                Selected Organisation does not exist on the CMS.
                Please contact the help center for assistance.
                """
            )

        program_id = data.get("program_id")
        try:
            Program.objects.get(pk=program_id)
        except ObjectDoesNotExist:
            raise ProviderException(
                """
                Selected Program does not exist on the CMS.
                Please contact the help center for assistance.
                """
            )

        facility_id = data.get("facility_id")
        try:
            Facility.objects.get(pk=facility_id)
        except ObjectDoesNotExist:
            raise ProviderException(
                """
                Selected Facility does not exist on the CMS.
                Please contact the help center for assistance.
                """
            )

        # unique username
        username = f'{data.get("username")}@{data.get("staff_id").split("-")[3]}'

        return dict(
            username=username,
            name=data.get("sub"),
            gender=data.get("gender").upper(),
            is_organisation_admin=data.get("is_organisation_admin"),
            is_program_admin=data.get("is_program_admin"),
            is_superuser=data.get("is_superuser"),
            organisation_id=organisation_id,
            program_id=program_id,
            staff_id=data.get("staff_id"),
            facility_id=facility_id,
        )


provider_classes = [MycarehubProvider]
