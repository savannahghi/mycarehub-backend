from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.snippets.models import register_snippet

from mycarehub.common.models import AbstractBase
from mycarehub.common.models.common_models import Address, Contact, Facility


@register_snippet
class Staff(AbstractBase):
    """ "
    Staff model is used to store staff details.
    """

    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    staff_number = models.CharField(max_length=255, blank=True, null=True)
    facilities = models.ManyToManyField(
        Facility, related_name="assigned_staff_members", blank=False
    )
    default_facility = models.ForeignKey(
        Facility,
        on_delete=models.PROTECT,
        related_name="assigned_staff",
        null=False,
        blank=False,
    )
    # a staff can have multiple unique identifiers
    identifiers = models.ManyToManyField(to="clients.Identifier", related_name="staff_identifiers")

    addresses = models.ManyToManyField(
        Address,
        related_name="staff_addresses",
        blank=True,
    )
    contacts = models.ManyToManyField(
        Contact,
        related_name="staff_contacts",
        blank=True,
    )

    def __str__(self):
        return f"{self.user.name} {self.staff_number}" if self.user else f"{self.staff_number}"


class ServiceRequest(AbstractBase):
    """
    ServiceRequest is used to consolidate service requests sent by staff.
    """

    class ServiceRequestType(models.TextChoices):
        STAFF_PIN_RESET = "STAFF_PIN_RESET", _("STAFF_PIN_RESET")

    class ServiceRequestStatus(models.TextChoices):
        PENDING = "PENDING", _("PENDING")
        RESOLVED = "RESOLVED", _("RESOLVED")

    staff = models.ForeignKey(Staff, on_delete=models.PROTECT)
    request_type = models.CharField(
        choices=ServiceRequestType.choices,
        max_length=36,
    )
    request = models.TextField()
    status = models.CharField(
        choices=ServiceRequestStatus.choices,
        max_length=36,
        default=ServiceRequestStatus.PENDING,
    )
    resolved_by = models.ForeignKey(
        Staff,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="service_request_resolved_by_admin_staff",
    )
    resolved_at = models.DateTimeField(null=True, blank=True)
    meta = models.JSONField(null=True, blank=True)
