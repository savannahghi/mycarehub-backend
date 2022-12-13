from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.search import index

from mycarehub.common.models import AbstractBase, Organisation


class Author(AbstractBase):
    """
    Author holds an author and their avatar (image).

        - the `title` field is used for the author's display name.
        - the `data` field contains the avatar (author's image).
    """

    name = models.CharField(max_length=128, help_text="Author's name (will be displayed publicly)")
    avatar = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="author_image",
        help_text="An optional author picture (will be displayed publicly)",
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("avatar"),
    ]

    def __str__(self):
        """Represent an author by their name."""
        return self.name

    class Meta(AbstractBase.Meta):
        verbose_name_plural = "authors"


class ContentItemCategory(index.Indexed, models.Model):
    """
    ContentItemCategory defines fixed (admin rather than author/editor defined)
    categories for content.

    It should be used to set up "predictable" categories e.g welcome content,
    diet, fitness, onboarding etc.
    """

    name = models.CharField(
        max_length=255,
        help_text="A standard name for a type of content e.g fitness, diet etc. "
        "These will be used in the user interface to group content so they "
        "should be chosen carefully.",
    )
    icon = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="content_item_category_icons",
        help_text="An optional icon for the content item category. "
        "This will be shown in the user interface so it should be chosen "
        "with care.",
    )

    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_related",
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("icon"),
    ]

    search_fields = [index.SearchField("name")]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "content item categories"
