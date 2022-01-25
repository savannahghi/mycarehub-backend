from django.contrib.auth import get_user_model
from django.db import models
from wagtail.snippets.models import register_snippet

from mycarehub.common.models import AbstractBase
from mycarehub.common.models.common_models import Facility


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

    def __str__(self) -> str:
        return f"{self.staff_number}"
