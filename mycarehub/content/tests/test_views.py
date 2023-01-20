import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse
from model_bakery import baker
from rest_framework import status

from mycarehub.clients.models import Client

from ..models import (
    Author,
    ContentBookmark,
    ContentItemCategory,
    ContentLike,
    ContentShare,
    ContentView,
)

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
    client_one = baker.make(Client)

    baker.make(
        ContentView,
        client=client_one,
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
    client_one = baker.make(Client)

    baker.make(
        ContentShare,
        client=client_one,
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
    client_one = baker.make(Client)

    baker.make(
        ContentLike,
        client=client_one,
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
    client_one = baker.make(Client)

    baker.make(
        ContentBookmark,
        client=client_one,
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

    client_one = baker.make(Client)

    response = client.post(
        url,
        data={
            "client": client_one.id,
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

    client_one = baker.make(Client)

    response = client.post(
        url,
        data={
            "client": client_one.id,
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

    client_one = baker.make(Client)

    response = client.post(
        url,
        data={
            "client": client_one.id,
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

    client_one = baker.make(Client)

    response = client.post(
        url,
        data={
            "client": client_one.id,
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


def test_author_snippet_list(user_with_all_permissions, client):
    client.force_login(user_with_all_permissions)
    url = reverse("wagtailsnippets_content_author:list")

    baker.make(Author, organisation=user_with_all_permissions.organisation)

    response = client.get(url)

    print(response.content.decode())
    assert response.status_code == status.HTTP_200_OK


def test_content_item_category_snippet_list(user_with_all_permissions, client):
    client.force_login(user_with_all_permissions)
    url = reverse("wagtailsnippets_content_contentitemcategory:list")

    baker.make(ContentItemCategory, organisation=user_with_all_permissions.organisation)

    response = client.get(url)

    print(response.content)
    assert response.status_code == status.HTTP_200_OK


def test_author_chooser_list(user_with_all_permissions, client):
    client.force_login(user_with_all_permissions)
    url = reverse("wagtailadmin_home")
    url = url + "author_chooser/"

    baker.make(Author, organisation=user_with_all_permissions.organisation)

    response = client.get(url)

    print(response.content)
    assert response.status_code == status.HTTP_200_OK


def test_add_media(user_with_all_permissions, client):
    client.force_login(user_with_all_permissions)
    url = reverse("wagtailmedia:add", kwargs={"media_type": "video"})

    video = SimpleUploadedFile("file.mp4", b"file_content", content_type="video/mp4")

    response = client.post(
        url,
        data={
            "title": "Test Video",
        },
        files={"file": video},
        content_type="application/json",
        accept="application/json",
        follow=True,
    )

    print(response.content)
    assert response.status_code == status.HTTP_200_OK
