import uuid

from django.conf import settings
from django.db.utils import ProgrammingError

DEFAULT_ORG_CODE = 1


def default_organisation():
    try:
        from mycarehub.common.models import Organisation  # intentional late import

        org, _ = Organisation.objects.get_or_create(
            code=DEFAULT_ORG_CODE,
            id=settings.DEFAULT_ORG_ID,
            defaults={
                "organisation_name": settings.ORGANISATION_NAME,
                "email_address": settings.ORGANISATION_EMAIL,
                "phone_number": settings.ORGANISATION_PHONE,
            },
        )
        return org.pk
    except (ProgrammingError, Exception):  # pragma: nocover
        # this will occur during initial migrations on a clean db
        return uuid.UUID(settings.DEFAULT_ORG_ID)


def default_program():
    try:
        from mycarehub.common.models import Program  # intentional late import

        org, _ = Program.objects.get_or_create(
            id=settings.DEFAULT_PROGRAM_ID,
            defaults={
                "name": f"{settings.ORGANISATION_NAME} Program",
            },
        )
        return org.pk
    except (ProgrammingError, Exception):  # pragma: nocover
        # this will occur during initial migrations on a clean db
        return uuid.UUID(settings.DEFAULT_PROGRAM_ID)
