import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from model_bakery import baker
from wagtail.admin.menu import MenuItem
from wagtail.models import Page, Site

from mycarehub.content.models import Author, ContentItem, ContentItemIndexPage, CustomMedia
from mycarehub.content.wagtail_hooks import (
    before_publish_page,
    chooser_show_organisation_pages_only,
    construct_homepage_summary_items,
    explorer_show_organisation_pages_only,
    get_global_admin_js,
    hide_explorer_menu_item_from_non_superuser,
    set_organisation_after_page_create,
    set_organisation_after_snippet_create,
    show_organisation_documents_only,
    show_organisation_images_only,
    show_organisation_media_only,
)
from mycarehub.home.models import HomePage

pytestmark = pytest.mark.django_db


def test_get_global_admin_js():
    admin_script = get_global_admin_js()
    assert "DOMContentLoaded" in admin_script


def test_before_publish_content_item_audio_video_no_media(
    request_with_user,
    content_item_with_tag_and_category,
):
    page = content_item_with_tag_and_category
    page.item_type = "AUDIO_VIDEO"
    page.save()
    page.refresh_from_db()
    assert page.featured_media.count() == 0
    assert page.item_type == "AUDIO_VIDEO"

    with pytest.raises(ValidationError) as c:
        before_publish_page(request_with_user, page)

    assert (
        "an AUDIO_VIDEO content item must have at least one video "
        "or audio file before publication"
    ) in str(c.value.messages)


def test_before_publish_content_item_pdf_document_no_document(
    request_with_user,
    content_item_with_tag_and_category,
):
    page = content_item_with_tag_and_category
    page.item_type = "PDF_DOCUMENT"
    page.save()
    page.refresh_from_db()
    assert page.documents.count() == 0
    assert page.item_type == "PDF_DOCUMENT"

    with pytest.raises(ValidationError) as c:
        before_publish_page(request_with_user, page)

    assert (
        "a PDF_DOCUMENT content item must have at least one document "
        "attached before publication"
    ) in str(c.value.messages)


def test_before_publish_non_content_item_page(request_with_user):
    site = Site.find_for_request(request_with_user)
    assert site is not None
    root = site.root_page

    # should not raise any exceptions
    before_publish_page(request_with_user, root)


def test_before_publish_content_item_article(
    request_with_user,
    content_item_with_tag_and_category,
):
    # there should be no exception
    before_publish_page(request=request_with_user, page=content_item_with_tag_and_category)


def test_set_organisation_after_page_create(
    request_with_user,
    content_item_index,
):
    root = Page.get_first_root_node()
    home = HomePage(
        title="Home",
        slug="index",
    )
    root.add_child(instance=home)
    root.save_revision().publish()

    set_organisation_after_page_create(request=request_with_user, page=content_item_index)

    set_organisation_after_page_create(request=request_with_user, page=home)


def test_set_content_item_program_after_page_create(
    request_with_user,
    content_item_index,
):
    # get a hero image
    hero = baker.make("content.CustomImage", _create_files=True)
    # set up a content item
    author = baker.make(Author)

    content_item = ContentItem(
        title="An article",
        slug="article-1",
        intro="intro",
        body="body",
        item_type="ARTICLE",
        date=timezone.now().date(),
        author=author,
        hero_image=hero,
    )

    content_item_index.add_child(instance=content_item)
    content_item_index.save_revision().publish()

    content_item.move(content_item_index, pos="last-child")

    set_organisation_after_page_create(request=request_with_user, page=content_item)


def test_explorer_show_organisation_pages_only(request_with_user, homepage, content_item_index):
    # get a hero image
    hero = baker.make("content.CustomImage", _create_files=True)

    # set up a content item
    author = baker.make(Author)
    content_item = ContentItem(
        title="An article",
        slug="article-1",
        intro="intro",
        body="body",
        item_type="ARTICLE",
        date=timezone.now().date(),
        author=author,
        hero_image=hero,
        organisation=request_with_user.user.organisation,
    )
    content_item_index.add_child(instance=content_item)
    content_item_index.save_revision().publish()

    content_item_index_two = ContentItemIndexPage(
        title="Content Item Index Two",
        slug="articlez",
        intro="content",
        organisation=request_with_user.user.organisation,
    )

    homepage.add_child(instance=content_item_index_two)
    homepage.save_revision().publish()

    pages = Page.objects.all()

    explorer_show_organisation_pages_only(
        parent_page=Page.get_first_root_node(), pages=pages, request=request_with_user
    )

    explorer_show_organisation_pages_only(
        parent_page=content_item_index, pages=ContentItem.objects.all(), request=request_with_user
    )


def test_chooser_show_organisation_pages_only(
    request_with_user, content_item_with_tag_and_category, content_item_index
):
    # get a hero image
    hero = baker.make("content.CustomImage", _create_files=True)

    # set up a content item
    author = baker.make(Author)
    content_item = ContentItem(
        title="An article",
        slug="article-1",
        intro="intro",
        body="body",
        item_type="ARTICLE",
        date=timezone.now().date(),
        author=author,
        hero_image=hero,
        organisation=request_with_user.user.organisation,
    )
    content_item_index.add_child(instance=content_item)
    content_item_index.save_revision().publish()

    pages = Page.objects.all()

    chooser_show_organisation_pages_only(pages=pages, request=request_with_user)

    chooser_show_organisation_pages_only(
        pages=ContentItem.objects.all(), request=request_with_user
    )


def test_set_organisation_after_snippet_create(request_with_user):
    author = baker.make(Author)

    set_organisation_after_snippet_create(request=request_with_user, instance=author)

    assert author.organisation == request_with_user.user.organisation


def test_show_organisation_media_only(request_with_user):
    baker.make(CustomMedia, organisation=request_with_user.user.organisation)

    show_organisation_media_only(media=CustomMedia.objects.all(), request=request_with_user)


def test_hide_explorer_menu_item_from_non_superuser(request_with_user, admin_user):
    hide_explorer_menu_item_from_non_superuser(
        request=request_with_user, menu_items=[MenuItem("settings", "sample/")]
    )

    request_with_user.user = admin_user

    hide_explorer_menu_item_from_non_superuser(
        request=request_with_user, menu_items=[MenuItem("settings", "sample/")]
    )


def test_show_organisation_documents_only(request_with_user):
    documents = show_organisation_documents_only([], request_with_user)

    assert len(documents) == 0


def test_show_organisation_images_only(request_with_user):
    images = show_organisation_images_only([], request_with_user)

    assert len(images) == 0


def test_construct_homepage_summary_items(request_with_user):
    construct_homepage_summary_items(request=request_with_user, summary_items=[])
