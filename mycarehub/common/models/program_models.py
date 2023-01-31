from django.db import models

from .base_models import AbstractBase
from .common_models import Facility


class Program(AbstractBase):

    name = models.TextField(max_length=100, unique=True)
    facilities = models.ManyToManyField(Facility, blank=True, related_name="programs")

    class Meta:
        unique_together = (
            "name",
            "organisation",
        )

    def __str__(self):
        return f"{self.name}"
