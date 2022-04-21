from datetime import date

from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from mycarehub.clients.models import ClientType
from mycarehub.common.models.common_models import Facility


def validate_date_past(value):
    if not isinstance(value, date):
        raise ValidationError(
            _("%(value)s is not a date"),
            params={"value": value},
        )

    if value > timezone.now().date():
        raise ValidationError(
            _("%(value)s is a date that is in the future"),
            params={"value": value},
        )


def get_facility_choices():
    return [(facility.name) for facility in Facility.objects.all()]


def get_client_types():
    return [(client_type) for client_type in ClientType.choices]
