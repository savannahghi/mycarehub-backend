from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page


class HomePage(Page):
    """
    This is the entry point for the CMS website.
    """

    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body", classname="full"),
    ]
    parent_page_types = ["wagtailcore.page"]
    subpage_types = [
        "content.ContentItemIndexPage",
    ]

    def get_context(self, request):
        # Update context to include only published items, in reverse-chronological
        # order
        context = super().get_context(request)
        items = self.get_children().live().order_by("-first_published_at")
        context["items"] = items
        return context
