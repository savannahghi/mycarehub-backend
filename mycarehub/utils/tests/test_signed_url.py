from django.conf import settings

from ..signed_url import generate_media_blob_name, generate_media_name, generate_signed_upload_url


def test_generate_signed_upload_url():
    name = generate_media_name(file_name="Test File.mp4")
    link = generate_signed_upload_url(
        bucket_name=settings.GS_BUCKET_NAME,
        blob_name=name,
        content_type="video/mp4",
    )

    assert link != ""


def test_generate_media_name():
    file_name = "Test File.mp4"
    name = generate_media_name(file_name=file_name)

    assert name == "media/Test_File.mp4"


def test_generate_media_blob_name():
    file_name = "Test File.mp4"

    name = generate_media_blob_name(file_name=file_name)

    assert name == "media/media/Test_File.mp4"
