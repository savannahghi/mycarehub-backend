from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.api import APIField
from wagtail.models import Page
from wagtail.search import index

from mycarehub.common.models import Organisation, Program


class FafanukaContentItem(Page):
    """
    A `FafanukaContentItem` represents the content periodically
    sent to Fafanuka subscribers.
    """

    class ItemTypes(models.TextChoices):
        GENERAL_TIPS = "GENERAL DIABETES TIPS"
        TYPE_1 = "TYPE 1 DIABETES "
        TYPE_2 = "TYPE 2 DIABETES "
        GESTATIONAL = "GESTATIONAL DIABETES "

    # basic properties that each post has
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_related",
    )

    program = models.ForeignKey(
        Program,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_related",
    )

    date = models.DateField(
        "Post date",
        help_text="This will be shown to readers as the publication date",
    )
    category = models.CharField(
        max_length=64,
        choices=ItemTypes.choices,
    )
    english_content = models.CharField(
        max_length=160,
    )
    kiswahili_content = models.CharField(
        max_length=160,
    )
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("date"),
                FieldPanel("category"),
            ],
            heading="About",
        ),
        FieldPanel("english_content", classname="full"),
        FieldPanel("kiswahili_content", classname="full"),
    ]

    # these fields determine the content that is indexed for search purposes
    search_fields = Page.search_fields + [
        index.SearchField("category"),
        index.SearchField("english_content"),
        index.SearchField("kiswahili_content"),
    ]

    # this configuration allows these custom fields to be available over the API
    api_fields = [
        APIField("date"),
        APIField("category"),
        APIField("english_content"),
        APIField("kiswahili_content"),
    ]

    # limit the parent page types
    parent_page_type = [
        "content.ContentItemIndexPage",
    ]

    subpage_types = []  # type: ignore
