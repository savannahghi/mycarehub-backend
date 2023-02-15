from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .base_models import AbstractBase
from .common_models import Facility


class ContentSequence(models.TextChoices):
    GRADUAL = "GRADUAL", _("Gradual")
    INSTANT = "INSTANT", _("Instant")


class Program(AbstractBase):
    name = models.TextField(max_length=100, unique=True)
    facilities = models.ManyToManyField(Facility, blank=True, related_name="programs")
    content_sequence = models.CharField(
        choices=ContentSequence.choices,
        max_length=16,
        default=ContentSequence.INSTANT,
        help_text="How content is served in the program",
    )
    start_date = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = (
            "name",
            "organisation",
        )

    def __str__(self):
        return f"{self.name}"
