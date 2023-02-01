import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse
from model_bakery import baker
from rest_framework import status

from mycarehub.clients.models import Client
from mycarehub.content.models import CustomDocument, CustomImage, CustomMedia

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


def test_custom_image_index_view(admin_user, user_with_all_permissions, client):
    admin_user.organisation = user_with_all_permissions.organisation
    client.force_login(admin_user)
    url = reverse("wagtailimages:index")

    baker.make(
        CustomImage, organisation=user_with_all_permissions.organisation, _create_files=True
    )
    baker.make(CustomImage, _create_files=True)

    response = client.get(url)

    print(response.content)
    assert response.status_code == status.HTTP_200_OK


def test_custom_document_index_view(admin_user, user_with_all_permissions, client):
    admin_user.organisation = user_with_all_permissions.organisation
    client.force_login(admin_user)
    url = reverse("wagtaildocs:index")

    baker.make(
        CustomDocument, organisation=user_with_all_permissions.organisation, _create_files=True
    )
    baker.make(CustomDocument, _create_files=True)

    response = client.get(url)

    print(response.content)
    assert response.status_code == status.HTTP_200_OK


def test_custom_media_index_view(admin_user, user_with_all_permissions, client):
    admin_user.organisation = user_with_all_permissions.organisation
    client.force_login(admin_user)
    url = reverse("wagtailmedia:index")

    baker.make(
        CustomMedia, organisation=user_with_all_permissions.organisation, _create_files=True
    )
    baker.make(CustomMedia, _create_files=True)

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

    params_response = client.get(
        url,
        {"ordering": "title", "collection_id": 1, "q": "test", "tag": "sample"},
        HTTP_X_REQUESTED_WITH="XMLHttpRequest",
    )
    assert params_response.status_code == status.HTTP_200_OK


def test_custom_image_add(admin_user, user_with_all_permissions, client):
    client.force_login(admin_user)
    url = reverse("wagtailimages:add")

    image = SimpleUploadedFile("file.jpeg", b"file_content", content_type="image/jpeg")

    response = client.post(
        url,
        data={
            "name": "Test Image",
        },
        files={"file", image},
    )

    print(response.content)

    assert response.status_code == status.HTTP_200_OK


def test_custom_document_add(admin_user, user_with_all_permissions, client):
    client.force_login(admin_user)
    url = reverse("wagtaildocs:add")

    doc = SimpleUploadedFile("file.pdf", b"file_content", content_type="application/pdf")

    response = client.post(
        url,
        data={
            "name": "Test Document",
        },
        files={"file", doc},
    )

    print(response.content)

    assert response.status_code == status.HTTP_200_OK


def test_custom_image_add_existing(admin_user, user_with_all_permissions, client):
    client.force_login(admin_user)

    image = baker.make(
        CustomImage, organisation=user_with_all_permissions.organisation, _create_files=True
    )
    # /admin/images/multiple/2/
    url = f"/admin/images/multiple/{image.id}/"

    response = client.post(
        url,
        data={
            "name": "Test Image",
        },
        files={"file", image.file},
    )

    print(response.content)

    assert response.status_code == status.HTTP_200_OK


def test_custom_document_add_existing(admin_user, user_with_all_permissions, client):
    client.force_login(admin_user)

    doc = baker.make(
        CustomDocument, organisation=user_with_all_permissions.organisation, _create_files=True
    )
    # /admin/documents/multiple/2/
    url = f"/admin/documents/multiple/{doc.id}/"

    response = client.post(
        url,
        data={
            "name": "Test Document",
        },
        files={"file", doc.file},
    )

    print(response.content)

    assert response.status_code == status.HTTP_200_OK
