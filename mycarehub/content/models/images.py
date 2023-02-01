# models.py
from django.db import models
from wagtail.images.models import AbstractImage, AbstractRendition, Image

from mycarehub.common.models import Organisation


class CustomImage(AbstractImage):
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_related",
    )

    admin_form_fields = Image.admin_form_fields

    class Meta(AbstractImage.Meta):
        permissions = [
            ("choose_image", "Can choose image"),
        ]


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(CustomImage, on_delete=models.CASCADE, related_name="renditions")

    class Meta:
        unique_together = (("image", "filter_spec", "focal_point_key"),)
