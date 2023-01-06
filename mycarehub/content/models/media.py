from django.db import models
from wagtailmedia.models import AbstractMedia

from mycarehub.common.models import Organisation


class CustomMedia(AbstractMedia):

    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_related",
    )
