import pytest
from django.utils import timezone
from model_bakery import baker
from wagtail.models import Page, Site

from mycarehub.content.models import Author, ContentItem, CustomMedia
from mycarehub.content.models.sms import SMSContentItem
from mycarehub.content.wagtail_hooks import (
    before_publish_page,
    chooser_show_organisation_pages_only,
    construct_homepage_summary_items,
    get_global_admin_js,
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


def test_set_sequence_number_after_page_create(
    request_with_user,
    content_item_index,
    sms_category,
    sms_tag,
):
    sms_content_item = SMSContentItem(
        body="Hello is some sample content for testing purposes",
        category=sms_category,
        tag=sms_tag,
    )

    content_item_index.add_child(instance=sms_content_item)
    content_item_index.save_revision().publish()

    set_organisation_after_page_create(request=request_with_user, page=sms_content_item)

    sms = SMSContentItem.objects.all().first()
    assert sms.sequence_number == 1


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


def test_set_organisation_after_snippet_create(request_with_user):
    author = baker.make(Author)

    set_organisation_after_snippet_create(request=request_with_user, instance=author)

    assert author.organisation == request_with_user.user.organisation


def test_show_organisation_media_only(request_with_user):
    baker.make(CustomMedia, organisation=request_with_user.user.organisation)

    show_organisation_media_only(media=CustomMedia.objects.all(), request=request_with_user)


def test_show_organisation_documents_only(request_with_user):
    documents = show_organisation_documents_only([], request_with_user)

    assert len(documents) == 0


def test_show_organisation_images_only(request_with_user):
    images = show_organisation_images_only([], request_with_user)

    assert len(images) == 0


def test_construct_homepage_summary_items(request_with_user):
    construct_homepage_summary_items(request=request_with_user, summary_items=[])
