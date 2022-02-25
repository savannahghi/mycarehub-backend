import datetime

from google.cloud import storage  # type: ignore[attr-defined]


def generate_signed_upload_url(bucket_name, blob_name, content_type):
    """
    Generates a v4 signed URL for uploading a blob using HTTP PUT.
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    url = blob.generate_signed_url(
        version="v4",
        # TODO: set shorter time or get from config
        expiration=datetime.timedelta(hours=1),
        method="PUT",
        content_type=content_type,
    )

    return url


def generate_media_name(file_name: str) -> str:
    """Camel cased media name

    Addition of "media" is due to the "upload_to" argument in the media model used
        -  `file = models.FileField(upload_to="media", verbose_name=_("file"))`
    """
    name = file_name.replace(" ", "_")

    return f"media/{name}"


def generate_media_blob_name(file_name: str) -> str:
    """
    created in this format
    {the media root URL}/{Upload to directory defined in file field}/{camel cased file name}

    It is specific to wagtailmedia media model
    """

    return f"media/{generate_media_name(file_name)}"
