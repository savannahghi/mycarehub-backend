import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework import status

from mycarehub.common.models import Program
from mycarehub.content.models import ContentItemCategory

pytestmark = pytest.mark.django_db


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


def test_category_get_all_categories(
    content_item_with_tag_and_category,
    request_with_user,
    client,
):
    assert content_item_with_tag_and_category is not None
    assert content_item_with_tag_and_category.categories.count() == 1
    assert content_item_with_tag_and_category.categories.filter().count() == 1

    client.force_login(request_with_user.user)
    url = (
        reverse("wagtailapi:pages:listing")
        + "?type=content.ContentItem&fields=*&order=-first_published_at"
    )
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["meta"]["total_count"] == 1


def test_category_name_filter_found_categories(
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
        + "?type=content.ContentItem&fields=*&category_name=a-valid-category"
    )
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["meta"]["total_count"] == 1


def test_category_with_content_filter(
    content_item_with_tag_and_category,
    request_with_user,
    client,
):
    assert content_item_with_tag_and_category is not None
    assert content_item_with_tag_and_category.categories.count() == 1
    assert content_item_with_tag_and_category.categories.filter(id=999_999).count() == 1

    client.force_login(request_with_user.user)
    url = reverse("api:contentitemcategory-list") + "?has_content=True"
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["count"] == 1


def test_category_with_program_filter(
    request_with_user,
    client,
):
    icon_livin = baker.make("wagtailimages.Image", _create_files=True)

    program_set_one = baker.make(Program, _quantity=3)
    program_set_two = baker.make(Program, _quantity=3)

    category_one = baker.make(ContentItemCategory, programs=program_set_one, icon=icon_livin)
    category_one.save()
    category_one.programs.add(*program_set_one)
    assert category_one.programs.count() == 3

    category_two = baker.make(ContentItemCategory, programs=program_set_two, icon=icon_livin)
    category_two.save()
    category_two.programs.add(*program_set_two)
    assert category_two.programs.count() == 3

    program = program_set_one[0]

    client.force_login(request_with_user.user)
    url = reverse("api:contentitemcategory-list") + f"?program_id={program.id}"
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["count"] == 1
