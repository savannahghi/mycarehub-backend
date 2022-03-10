from django.db import models
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

    appointment_type = models.CharField(max_length=36)
    status = models.CharField(max_length=36)
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
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self) -> str:
        return f"{self.client} - {self.appointment_type} - {self.status}"
