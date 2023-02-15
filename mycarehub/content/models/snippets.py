from django import forms
from django.db import models
from modelcluster.fields import ParentalManyToManyField
from modelcluster.models import ClusterableModel
from wagtail.admin.forms import WagtailAdminModelForm
from wagtail.admin.panels import FieldPanel
from wagtail.search import index

from mycarehub.common.models import AbstractBase, Organisation, Program


class CustomSnippetForm(WagtailAdminModelForm):
    def __init__(self, *args, **kwargs):  # pragma: no cover
        super().__init__(*args, **kwargs)
        self.fields["programs"].queryset = self.for_user.organisation.common_program_related.all()


class Author(AbstractBase, ClusterableModel):
    """
    Author holds an author and their avatar (image).

        - the `title` field is used for the author's display name.
        - the `data` field contains the avatar (author's image).
    """

    name = models.CharField(max_length=128, help_text="Author's name (will be displayed publicly)")
    avatar = models.ForeignKey(
        "content.CustomImage",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="author_image",
        help_text="An optional author picture (will be displayed publicly)",
    )
    programs = ParentalManyToManyField(Program)

    panels = [
        FieldPanel("name"),
        FieldPanel("avatar"),
        FieldPanel("programs", widget=forms.CheckboxSelectMultiple),
    ]

    base_form_class = CustomSnippetForm

    def __str__(self):
        """Represent an author by their name."""
        return self.name

    def get_programs(self):
        return "\n".join([p.name for p in self.programs.all()])

    get_programs.admin_order_field = "programs"  # type: ignore
    get_programs.short_description = "Programs"  # type: ignore

    class Meta(AbstractBase.Meta):
        verbose_name_plural = "authors"


class ContentItemCategory(index.Indexed, ClusterableModel):
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
        "content.CustomImage",
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
    programs = ParentalManyToManyField(Program)

    panels = [
        FieldPanel("name"),
        FieldPanel("icon"),
        FieldPanel("programs", widget=forms.CheckboxSelectMultiple),
    ]

    search_fields = [index.SearchField("name"), index.FilterField("organisation_id")]

    base_form_class = CustomSnippetForm

    def __str__(self):
        return self.name

    def get_programs(self):
        return "\n".join([p.name for p in self.programs.all()])

    get_programs.admin_order_field = "programs"  # type: ignore
    get_programs.short_description = "Programs"  # type: ignore

    class Meta:
        verbose_name_plural = "content item categories"
