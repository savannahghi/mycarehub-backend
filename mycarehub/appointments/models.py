from django.db import models
from django.db.models.enums import TextChoices
from django.utils.translation import gettext_lazy as _

from mycarehub.clients.models import Client
from mycarehub.common.models import AbstractBase
from mycarehub.staff.models import Staff


class Appointment(AbstractBase):
    """
    Appointment stores information of a scheduled day and time
    for an client to be evaluated or treated by a physician
    or other licensed health care professional.

    It is referenced from the Open MRS appointment data model
    """

    class AppointmentStatus(TextChoices):
        SCHEDULED = "SCHEDULED", _("Scheduled")
        RESCHEDULED = "RESCHEDULED", _("Rescheduled")
        WAITING = "WAITING", _("Waiting")
        MISSED = "MISSED", _("Missed")
        COMPLETED = "COMPLETED", _("Completed")
        INCONSULTATION = "INCONSULTATION", _("In Consultation")
        WALKIN = "WALKIN", _("Walk In")
        CANCELLED = "CANCELLED", _("Cancelled")
        NEEDSRESCHEDULE = "NEEDSRESCHEDULE", _("Needs Reschedule")

    appointment_uuid = models.UUIDField(
        editable=False,
        null=True,
        blank=True,
        help_text=_("Identifier that is shared between KenyaEMR and MyCareHub"),
    )
    appointment_type = models.CharField(max_length=36)
    status = models.CharField(max_length=36, choices=AppointmentStatus.choices)
    reason = models.TextField(max_length=1024, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    staff = models.ForeignKey(Staff, on_delete=models.PROTECT, null=True, blank=True)
    provider = models.CharField(
        max_length=36,
        help_text=_(
            "Name of individual conducting the appointment for when the staff is not in our system"
        ),
        null=True,
        blank=True,
    )
    date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.client} - {self.appointment_type} - {self.status}"
