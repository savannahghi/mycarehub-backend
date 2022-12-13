from django.contrib.auth import get_user_model
from django.db import models

from mycarehub.common.models import AbstractBase
from mycarehub.common.models.common_models import Facility


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

    def __str__(self):
        return f"{self.user.name} {self.staff_number}" if self.user else f"{self.staff_number}"
