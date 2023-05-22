import threading

from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
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

    class OfferType(models.TextChoices):
        """The three different types of diabetes."""

        TYPE_1_DIABETES = "001032833390", _("TYPE 1 DIABETES")
        TYPE_2_DIABETES = "001032833389", _("TYPE 2 DIABETES")
        GESTATIONAL_DIABETES = "001032833393", _("GESTATIONAL DIABETES")
        GENERAL_TIPS = "001032833395", _("GENERAL")

    class SubGroup(models.IntegerChoices):
        """Diabetes content sub groups."""

        DIABETES_GENERAL_INFORMATION = 1, _("Diabetes General Information")
        DIABETES_AND_SCREENING = 2, _("Diabetes and Screening")
        DIABETES_MANAGEMENT = 3, _("Diabetes mangement")
        DIABETES_AND_PREGNANCY = 4, _("Diabetes and pregnancy")
        EXERCISE_AND_DIABETES = 5, _("Exercise and diabetes")
        DIABETES_AND_PREVENTION = 6, _("Diabetes and prevention")
        DIET_AND_NUTRITION = 7, _("Diabetes and nutrition")
        DIABETES_COMPLICATIONS = 8, _("Diabetes and complications")
        DIABETES_AND_SUPPORT = 9, _("Diabetes and support")
        DIABETES_AND_FOOTCARE = 10, _("Diabetes and footcare")

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
    offer = models.CharField(
        max_length=64,
        choices=OfferType.choices,
        default=OfferType.GENERAL_TIPS,
    )
    subgroup = models.IntegerField(
        choices=SubGroup.choices,
        default=SubGroup.DIABETES_GENERAL_INFORMATION,
    )
    sequence_number = models.IntegerField(null=True, blank=True)
    sequence = models.CharField(max_length=10, null=True, blank=True)
    swahili_content = models.TextField(max_length=160)
    english_content = models.TextField(max_length=160)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("offer"),
                FieldPanel("subgroup"),
            ],
            heading="About",
        ),
        FieldPanel("swahili_content"),
        FieldPanel("english_content"),
    ]

    # these fields determine the content that is indexed for search purposes
    search_fields = Page.search_fields + [
        index.SearchField("offer"),
        index.SearchField("english_content"),
        index.SearchField("swahili_content"),
    ]

    # this configuration allows these custom fields to be available over the API
    api_fields = [
        APIField("live"),
        APIField("organisation"),
        APIField("program"),
        APIField("offer"),
        APIField("subgroup"),
        APIField("sequence"),
        APIField("sequence_number"),
        APIField("english_content"),
        APIField("swahili_content"),
    ]

    # limit the parent page types
    parent_page_type = [
        "content.ContentItemIndexPage",
    ]

    subpage_types = []  # type: ignore

    def __str__(self):
        """Human readable model representation."""
        return f"{self.sequence} {self.title}"

    def generate_sequence_number(self):
        """Generate content sequence and sequence numbers."""
        if self.__class__.objects.filter(pk=self.pk, sequence__isnull=False):
            return

        filters = {
            "organisation": self.organisation,
            "program": self.program,
            "offer": self.offer,
        }
        seq = self.__class__.objects.filter(**filters).count()
        lock = threading.Lock()

        def increment_seq(lock):
            lock.acquire()
            nonlocal seq
            seq = seq + 1
            lock.release()

        thread = threading.Thread(target=increment_seq, args=(lock,))
        thread.start()
        thread.join()

        """Define the offer code to key mapping"""
        offercode_to_key_mapping = {
            self.OfferType.GENERAL_TIPS.value: 1,
            self.OfferType.TYPE_1_DIABETES.value: 2,
            self.OfferType.TYPE_2_DIABETES.value: 3,
            self.OfferType.GESTATIONAL_DIABETES.value: 4,
        }

        self.sequence_number = seq
        self.offercode_to_key_mapping = offercode_to_key_mapping
        self.sequence = f"{self.offercode_to_key_mapping[self.offer]}.{self.sequence_number}"

    def save(self, *args, **kwargs):
        """Override save method."""
        new_title = self.english_content[:30]
        self.slug = slugify(new_title)
        self.title = new_title
        super().save(*args, **kwargs)


# Assign default values to the slug and title field, in order to avoid validation errors
slug_field = FafanukaContentItem._meta.get_field("slug")
slug_field.default = "default-blank-slug"
title_field = FafanukaContentItem._meta.get_field("title")
title_field.default = "default title value"
