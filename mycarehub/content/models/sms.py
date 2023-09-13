import logging
import threading

from django import forms
from django.db import models
from django.utils.text import Truncator, slugify
from modelcluster.fields import ParentalManyToManyField
from wagtail.admin.panels import FieldPanel, FieldRowPanel, MultiFieldPanel, WagtailAdminPageForm
from wagtail.api import APIField
from wagtail.models import Page
from wagtail.search import index

from mycarehub.common.models import AbstractBase, Organisation, Program

LOGGER = logging.getLogger(__name__)


class SMSContentItemPageForm(WagtailAdminPageForm):
    def __init__(
        self, data=None, files=None, parent_page=None, subscription=None, *args, **kwargs
    ):  # pragma: no cover
        super().__init__(data, files, parent_page, subscription, *args, **kwargs)
        self.fields["category"].queryset = self.fields["category"].queryset.filter(
            organisation=self.for_user.organisation, programs=parent_page.specific.program
        )


class SMSContentItemCategory(AbstractBase):
    """Category associated with an SMS."""

    code = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=64)
    sequence_key = models.IntegerField()
    programs = ParentalManyToManyField(Program)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        unique_together = (
            "sequence_key",
            "code",
        )
        verbose_name_plural = "sms content item categories"

    panels = [
        FieldPanel("code"),
        FieldPanel("name"),
        FieldPanel("sequence_key"),
        FieldPanel("programs", widget=forms.CheckboxSelectMultiple),
    ]

    def get_programs(self):
        return "\n".join([p.name for p in self.programs.all()])


class SMSContentItemTag(AbstractBase):
    """Tag associated with an SMS."""

    name = models.CharField(max_length=64)
    code = models.IntegerField()
    programs = ParentalManyToManyField(Program)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "sms content item tags"
        unique_together = (
            "name",
            "code",
        )

    panels = [
        FieldPanel("name"),
        FieldPanel("code"),
        FieldPanel("programs", widget=forms.CheckboxSelectMultiple),
    ]

    def get_programs(self):
        return "\n".join([p.name for p in self.programs.all()])


class SMSContentItem(Page):
    """
    An `SMSContentItem` represents the content that
    is sent to sms subscribers.
    """

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

    category = models.ForeignKey(
        SMSContentItemCategory, on_delete=models.PROTECT, related_name="categories"
    )

    tag = models.ForeignKey(SMSContentItemTag, on_delete=models.PROTECT, related_name="tags")
    sequence_number = models.IntegerField(null=True, blank=True)
    sequence = models.CharField(max_length=10, null=True, blank=True)
    swahili_content = models.TextField(max_length=160)
    english_content = models.TextField(max_length=160)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("category"),
                        FieldPanel("tag"),
                    ]
                ),
            ],
            heading="About",
        ),
        FieldPanel("swahili_content"),
        FieldPanel("english_content"),
    ]

    # these fields determine the content that is indexed for search purposes
    search_fields = Page.search_fields + [
        index.SearchField("category"),
        index.SearchField("english_content"),
        index.SearchField("swahili_content"),
    ]

    base_form_class = SMSContentItemPageForm

    # this configuration allows these custom fields to be available over the API
    api_fields = [
        APIField("live"),
        APIField("organisation"),
        APIField("program"),
        APIField("category"),
        APIField("tag"),
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
            msg = "Sequence has already been set"
            LOGGER.info(msg)
            return

        filters = {
            "organisation": self.organisation,
            "program": self.program,
            "category": self.category,
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

        self.sequence_number = seq
        self.sequence = f"{self.category.sequence_key}.{self.sequence_number}"

    def save(self, *args, **kwargs):
        """Override save method.

        We replace the title to make it easier for users to
        keep track of their sms's.
        """
        if self._state.adding:
            self.generate_sequence_number()

        new_title = Truncator(self.english_content).chars(30)
        self.slug = slugify(new_title)
        self.title = new_title
        super().save(*args, **kwargs)
