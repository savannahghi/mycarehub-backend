from django.contrib.postgres.fields import ArrayField, IntegerRangeField
from django.db import models

from mycarehub.clients.models import Client, ClientType
from mycarehub.common.models.base_models import AbstractBase
from mycarehub.staff.models import Staff
from mycarehub.users.models import GenderChoices


class Community(AbstractBase):
    """
    A community represents details of a space/group consisting of clients and staff
    where they can share information, consult and get support.

    The community has options during creation which act as meta data for the community
    which defines the eligibility criteria for joining,especially for a client.
    """

    name = models.CharField(max_length=64)
    description = models.CharField(max_length=150)
    client_types = ArrayField(
        models.CharField(
            max_length=64,
            choices=ClientType.choices,
        ),
        null=False,
        blank=False,
    )
    gender = ArrayField(
        models.CharField(
            choices=GenderChoices.choices,
            max_length=16,
        ),
        help_text=("The allowed gender(s) for users joining the community"),
        null=True,
        blank=True,
    )
    ages = IntegerRangeField(
        null=True,
        blank=True,
        help_text=("The allowed age band for clients joining the community"),
    )
    invite_only = models.BooleanField(
        default=True,
        help_text=("Whether a client can join a community without invitation."),
    )
    discoverable = models.BooleanField(
        default=True,
        help_text=("Whether a community can be suggested to a client or not"),
    )
    clients = models.ManyToManyField(
        to=Client,
        blank=True,
    )
    staff = models.ManyToManyField(
        to=Staff,
        blank=True,
    )

    class Meta(AbstractBase.Meta):
        verbose_name_plural = "communities"

    def __str__(self):
        return f"{self.name}"


class PostingHour(AbstractBase):
    """Time range when members of a community can communicate."""

    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    start = models.TimeField()
    end = models.TimeField()

    def __str__(self):
        return f"{self.start} - {self.end}"
