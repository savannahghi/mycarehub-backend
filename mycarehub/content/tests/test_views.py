import pytest
from django.test import override_settings
from django.urls import reverse
from model_bakery import baker
from rest_framework import status

from ..models import ContentBookmark, ContentLike, ContentShare, ContentView

pytestmark = pytest.mark.django_db


def test_generate_signed_url_gcs_storage_backend(user_with_all_permissions, client):
    client.force_login(user_with_all_permissions)
    url = reverse("signed-url")

    response = client.post(
        url,
        data={"fileName": "Test File", "fileType": "video/mp4"},
        content_type="application/json",
        accept="application/json",
    )

    print(response.content)
    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    assert response_data["url"] is not None


@override_settings(DEFAULT_FILE_STORAGE="django.core.files.storage.FileSystemStorage")
def test_generate_signed_url_non_gcs_storage_backend(user_with_all_permissions, client):
    client.force_login(user_with_all_permissions)
    url = reverse("signed-url")

    response = client.post(
        url,
        data={"fileName": "Test File", "fileType": "video/mp4"},
        content_type="application/json",
        accept="application/json",
    )

    print(response.content)
    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    assert response_data["url"] == ""


def test_content_category_list_view(
    content_item_with_tag_and_category, user_with_all_permissions, client
):
    client.force_login(user_with_all_permissions)
    url = reverse("api:contentitemcategory-list")

    response = client.get(
        url,
        content_type="application/json",
        accept="application/json",
    )

    print(response.content)
    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    assert response_data["count"] == 1


def test_content_view_list_view(
    content_item_with_tag_and_category, user_with_all_permissions, client
):
    baker.make(
        ContentView,
        user=user_with_all_permissions,
        content_item=content_item_with_tag_and_category,
    )
    client.force_login(user_with_all_permissions)
    url = reverse("api:contentview-list")

    response = client.get(
        url,
        content_type="application/json",
        accept="application/json",
    )

    print(response.content)
    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    assert response_data["count"] == 1


def test_content_share_list_view(
    content_item_with_tag_and_category, user_with_all_permissions, client
):
    baker.make(
        ContentShare,
        user=user_with_all_permissions,
        content_item=content_item_with_tag_and_category,
    )
    client.force_login(user_with_all_permissions)
    url = reverse("api:contentshare-list")

    response = client.get(
        url,
        content_type="application/json",
        accept="application/json",
    )

    print(response.content)
    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    assert response_data["count"] == 1


def test_content_like_list_view(
    content_item_with_tag_and_category, user_with_all_permissions, client
):
    baker.make(
        ContentLike,
        user=user_with_all_permissions,
        content_item=content_item_with_tag_and_category,
    )
    client.force_login(user_with_all_permissions)
    url = reverse("api:contentlike-list")

    response = client.get(
        url,
        content_type="application/json",
        accept="application/json",
    )

    print(response.content)
    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    assert response_data["count"] == 1


def test_content_bookmark_list_view(
    content_item_with_tag_and_category, user_with_all_permissions, client
):
    baker.make(
        ContentBookmark,
        user=user_with_all_permissions,
        content_item=content_item_with_tag_and_category,
    )
    client.force_login(user_with_all_permissions)
    url = reverse("api:contentbookmark-list")

    response = client.get(
        url,
        content_type="application/json",
        accept="application/json",
    )

    print(response.content)
    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    assert response_data["count"] == 1


def test_content_view_create_view(
    content_item_with_tag_and_category, user_with_all_permissions, client
):
    client.force_login(user_with_all_permissions)
    url = reverse("api:contentview-list")

    response = client.post(
        url,
        data={
            "user": user_with_all_permissions.id,
            "content_item": content_item_with_tag_and_category.id,
        },
        content_type="application/json",
        accept="application/json",
    )

    print(response.content)
    assert response.status_code == status.HTTP_201_CREATED

    response_data = response.json()
    assert response_data["id"] != ""


def test_content_share_create_view(
    content_item_with_tag_and_category, user_with_all_permissions, client
):
    client.force_login(user_with_all_permissions)
    url = reverse("api:contentshare-list")

    response = client.post(
        url,
        data={
            "user": user_with_all_permissions.id,
            "content_item": content_item_with_tag_and_category.id,
        },
        content_type="application/json",
        accept="application/json",
    )

    print(response.content)
    assert response.status_code == status.HTTP_201_CREATED

    response_data = response.json()
    assert response_data["id"] != ""


def test_content_like_create_view(
    content_item_with_tag_and_category, user_with_all_permissions, client
):
    client.force_login(user_with_all_permissions)
    url = reverse("api:contentlike-list")

    response = client.post(
        url,
        data={
            "user": user_with_all_permissions.id,
            "content_item": content_item_with_tag_and_category.id,
        },
        content_type="application/json",
        accept="application/json",
    )

    print(response.content)
    assert response.status_code == status.HTTP_201_CREATED

    response_data = response.json()
    assert response_data["id"] != ""


def test_content_bookmark_create_view(
    content_item_with_tag_and_category, user_with_all_permissions, client
):
    client.force_login(user_with_all_permissions)
    url = reverse("api:contentbookmark-list")

    response = client.post(
        url,
        data={
            "user": user_with_all_permissions.id,
            "content_item": content_item_with_tag_and_category.id,
        },
        content_type="application/json",
        accept="application/json",
    )

    print(response.content)
    assert response.status_code == status.HTTP_201_CREATED

    response_data = response.json()
    print(response_data)
    assert response_data["id"] != ""
