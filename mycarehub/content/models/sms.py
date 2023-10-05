import logging
import threading
import uuid

from django import forms
from django.db import models
from django.utils.text import Truncator, slugify
from modelcluster.fields import ParentalManyToManyField
from modelcluster.models import ClusterableModel
from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.admin.panels import FieldPanel, FieldRowPanel, MultiFieldPanel
from wagtail.api import APIField
from wagtail.models import Page
from wagtail.search import index

from mycarehub.common.models import Organisation, Program
from mycarehub.content.models.snippets import CustomSnippetForm

LOGGER = logging.getLogger(__name__)


class SMSContentItemPageForm(WagtailAdminPageForm):
    def __init__(
        self, data=None, files=None, parent_page=None, subscription=None, *args, **kwargs
    ):  # pragma: no cover
        super().__init__(data, files, parent_page, subscription, *args, **kwargs)
        self.fields["category"].queryset = self.fields["category"].queryset.filter(
            organisation=self.for_user.organisation, programs=parent_page.specific.program_id
        )
        self.fields["tag"].queryset = self.fields["tag"].queryset.filter(
            organisation=self.for_user.organisation, programs=parent_page.specific.program_id
        )


class SMSContentItemCategory(ClusterableModel):
    """Category associated with an SMS."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(
        max_length=32,
        unique=True,
        help_text="A code that will be used to uniquely identify a category",
    )
    name = models.CharField(
        max_length=64, help_text="This name will be displayed while creating sms content"
    )
    sequence_key = models.IntegerField(
        help_text="A pre-determined value to be used while sequencing content under this category"
    )
    programs = ParentalManyToManyField(
        Program, help_text="Select a program to assign this category"
    )
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_related",
    )
    base_form_class = CustomSnippetForm

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


class SMSContentItemTag(ClusterableModel):
    """Tag associated with an SMS."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=64, help_text="This name will be displayed when creating sms content"
    )
    code = models.IntegerField(
        help_text="A pre-determined value that will be used to uniquely identify a tag"
    )
    programs = ParentalManyToManyField(Program, help_text="Select a program to assign this tag")
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_related",
    )
    base_form_class = CustomSnippetForm

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
        SMSContentItemCategory,
        on_delete=models.PROTECT,
        related_name="categories",
        help_text="Category to associate content with",
    )

    tag = models.ForeignKey(
        SMSContentItemTag,
        on_delete=models.PROTECT,
        related_name="tags",
        help_text="Tag to associate content with",
    )
    sequence_number = models.IntegerField(null=True, blank=True)
    sequence = models.CharField(max_length=10, null=True, blank=True)
    content = models.TextField(
        max_length=160, help_text="Write out the body of the content to be sent to subscribers"
    )

    base_form_class = SMSContentItemPageForm

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("category", widget=forms.Select),
                        FieldPanel("tag", widget=forms.Select),
                    ]
                ),
            ],
            heading="About",
        ),
        FieldPanel("content"),
    ]

    # these fields determine the content that is indexed for search purposes
    search_fields = Page.search_fields + [
        index.SearchField("category"),
        index.SearchField("content"),
    ]

    # this configuration allows these custom fields to be available over the API
    api_fields = [
        APIField("live"),
        APIField("organisation"),
        APIField("program"),
        APIField("category"),
        APIField("tag"),
        APIField("sequence"),
        APIField("sequence_number"),
        APIField("content"),
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
        new_title = Truncator(self.content).chars(30)
        self.slug = slugify(new_title)
        self.title = new_title
        super().save(*args, **kwargs)
