from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from wagtail.core import hooks
from wagtail.documents import get_document_model
from wagtail.images import get_image_model
from wagtail.snippets.models import register_snippet

from mycarehub.home.models import HomePage

from .models import Author, ContentItem, ContentItemCategory
from .views import AuthorSnippetViewSet, ContentItemCategorySnippetViewSet, author_chooser_viewset


@hooks.register("insert_global_admin_js")
def get_global_admin_js():
    return mark_safe(
        r"""
    <script>
    window.addEventListener('DOMContentLoaded', function () {
        document.addEventListener('wagtail:images-upload', function(event) {
            var newTitle = (event.detail.data.title || '').replace(/[^a-zA-Z0-9\s-]/g, "");
            event.detail.data.title = newTitle;
        });

        document.addEventListener('wagtail:documents-upload', function(event) {
            var extension = (event.detail.filename.match(/\.([^.]*?)(?=\?|#|$)/) || [''])[1];
            var newTitle = '(' + extension.toUpperCase() + ') ' + (event.detail.data.title || '');
            event.detail.data.title = newTitle;
        });
    });
    </script>
    """
    )


@hooks.register("before_publish_page")
def before_publish_page(request, page):
    """
    Audio_Video type pages must have media linked before publishing.

    Document type pages must have documents linked before publishing.
    """

    if page.specific_class == ContentItem:
        if page.item_type == "AUDIO_VIDEO" and page.featured_media.count() == 0:
            msg = (
                "an AUDIO_VIDEO content item must have at least one video "
                "or audio file before publication"
            )
            raise ValidationError(msg)

        if page.item_type == "PDF_DOCUMENT" and page.documents.count() == 0:
            msg = (
                "a PDF_DOCUMENT content item must have at least one document "
                "attached before publication"
            )
            raise ValidationError(msg)


@hooks.register("after_create_page")
def set_organisation_after_page_create(request, page):
    if not hasattr(page, "organisation"):
        return

    page.organisation = request.user.organisation

    if page.specific_class == ContentItem:
        index = page.get_parent()
        page.program = index.program

    page.save()


@hooks.register("construct_explorer_page_queryset")
def explorer_show_organisation_pages_only(parent_page, pages, request):
    # TODO: this should be optimized :-)
    if parent_page.slug == "root":
        for page in pages:
            if page.specific_class == HomePage:
                pages = page.get_children()

        for page in pages:
            if page.specific.organisation != request.user.organisation:
                pages = pages & pages.not_page(page)

    return pages


@hooks.register("construct_page_chooser_queryset")
def chooser_show_organisation_pages_only(pages, request):
    for page in pages:
        if not hasattr(page, "organisation"):
            pages = pages & pages.not_page(page)
            continue

        if hasattr(page, "organisation") and page.organisation != request.user.organisation:
            pages = pages & pages.not_page(page)

    return pages


register_snippet(Author, viewset=AuthorSnippetViewSet)
register_snippet(ContentItemCategory, viewset=ContentItemCategorySnippetViewSet)


@hooks.register("after_create_snippet")
def set_organisation_after_snippet_create(request, instance):
    instance.organisation = request.user.organisation
    instance.save()


@hooks.register("construct_media_chooser_queryset")
def show_organisation_media_only(media, request):
    media = media.filter(organisation=request.user.organisation)

    return media


@hooks.register("register_admin_viewset")
def register_author_chooser_viewset():
    return author_chooser_viewset


@hooks.register("construct_main_menu")
def hide_explorer_menu_item_from_non_superuser(request, menu_items):
    if not request.user.is_superuser:
        menu_items[:] = [item for item in menu_items if item.name not in ["settings", "reports"]]


@hooks.register("construct_homepage_summary_items")
def construct_homepage_summary_items(request, summary_items):
    summary_items.clear()


@hooks.register("construct_document_chooser_queryset")
def show_organisation_documents_only(documents, request):
    documents = get_document_model().objects.filter(organisation=request.user.organisation)

    return documents


@hooks.register("construct_image_chooser_queryset")
def show_organisation_images_only(images, request):
    images = get_image_model().objects.filter(organisation=request.user.organisation)

    return images
