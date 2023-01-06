from django.db import models

from .base_models import AbstractBase


class Program(AbstractBase):

    name = models.TextField(max_length=100, unique=True)

    class Meta:
        unique_together = (
            "name",
            "organisation",
        )

    def __str__(self):
        return f"{self.name}"
