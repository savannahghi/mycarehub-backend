# models.py
from django.db import models
from wagtail.documents.models import AbstractDocument, Document

from mycarehub.common.models import Organisation


class CustomDocument(AbstractDocument):
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_related",
    )

    admin_form_fields = Document.admin_form_fields
