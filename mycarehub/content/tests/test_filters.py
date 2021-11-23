import pytest
from django.urls import reverse
from django.utils import timezone
from model_bakery import baker
from rest_framework import status
from taggit.models import Tag
from wagtail.core.models import Page, Site

from mycarehub.content.models import Author, ContentItem, ContentItemCategory, ContentItemIndexPage
from mycarehub.home.models import HomePage

pytestmark = pytest.mark.django_db


@pytest.fixture
def content_item_with_tag_and_category(request_with_user):
    # get the root page
    site = Site.find_for_request(request_with_user)
    assert site is not None
    root = site.root_page
    assert root is not None

    # set up a home page
    home = HomePage(
        title="Home",
        slug="index",
    )
    root.add_child(instance=home)
    root.save_revision().publish()

    # set up a content item index page
    content_item_index = ContentItemIndexPage(
        title="Content Item Index",
        slug="articles",
        intro="content",
    )
    home.add_child(instance=content_item_index)
    home.save_revision().publish()

    # get a hero image
    hero = baker.make("wagtailimages.Image", _create_files=True)

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

    # add a category
    icon = baker.make("wagtailimages.Image", _create_files=True)
    cat = baker.make(ContentItemCategory, id=999_999, name="a valid category", icon=icon)
    content_item.categories.add(cat)
    content_item.save()
    assert ContentItem.objects.filter(categories__id=cat.pk).count() == 1

    # add a tag
    tag = baker.make(Tag, name="a-valid-tag")  # expect slug a-valid-tag
    content_item.tags.add(tag)
    content_item.save()
    assert ContentItem.objects.filter(tags__name="a-valid-tag").count() == 1

    # sanity checks
    assert (
        Page.objects.all().public().live().count() >= 4
    )  # root, home, content index, content item
    assert ContentItem.objects.all().public().live().count() == 1

    # return the initialized content item
    content_item.save_revision().publish()
    return content_item


def test_tag_filter_found_tags(
    content_item_with_tag_and_category,
    request_with_user,
    client,
):
    assert content_item_with_tag_and_category is not None
    assert content_item_with_tag_and_category.tags.count() == 1
    assert content_item_with_tag_and_category.tags.filter(name="a-valid-tag").count() == 1

    client.force_login(request_with_user.user)
    url = (
        reverse("wagtailapi:pages:listing")
        + "?type=content.ContentItem&fields=*&order=-first_published_at&tag=a-valid-tag"
    )
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["meta"]["total_count"] == 1


def test_tag_filter_absent_tags(
    content_item_with_tag_and_category,
    request_with_user,
    client,
):
    assert content_item_with_tag_and_category is not None
    assert content_item_with_tag_and_category.tags.count() == 1
    assert content_item_with_tag_and_category.tags.filter(name="not-a-valid-tag").count() == 0

    client.force_login(request_with_user.user)
    url = (
        reverse("wagtailapi:pages:listing")
        + "?type=content.ContentItem&fields=*&order=-first_published_at&tag=not-a-valid-tag"
    )
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["meta"]["total_count"] == 0


def test_category_filter_found_categories(
    content_item_with_tag_and_category,
    request_with_user,
    client,
):
    assert content_item_with_tag_and_category is not None
    assert content_item_with_tag_and_category.categories.count() == 1
    assert content_item_with_tag_and_category.categories.filter(id=999_999).count() == 1

    client.force_login(request_with_user.user)
    url = (
        reverse("wagtailapi:pages:listing")
        + "?type=content.ContentItem&fields=*&order=-first_published_at&category=999999"
    )
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["meta"]["total_count"] == 1


def test_category_filter_absent_categories(
    content_item_with_tag_and_category,
    request_with_user,
    client,
):
    assert content_item_with_tag_and_category is not None
    assert content_item_with_tag_and_category.categories.count() == 1
    assert content_item_with_tag_and_category.categories.filter(id=999_999).count() == 1

    client.force_login(request_with_user.user)
    url = (
        reverse("wagtailapi:pages:listing")
        + "?type=content.ContentItem&fields=*&order=-first_published_at&category=87654321"
    )
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["meta"]["total_count"] == 0
