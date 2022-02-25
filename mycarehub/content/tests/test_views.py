import pytest
from django.test import override_settings
from django.urls import reverse
from rest_framework import status

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
