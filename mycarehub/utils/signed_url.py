import datetime

from django.conf import settings
from google.auth import compute_engine
from google.auth.exceptions import TransportError
from google.auth.transport import requests
from google.cloud import storage  # type: ignore[attr-defined]
from urllib3.exceptions import NewConnectionError


def generate_signed_upload_url(bucket_name, blob_name, content_type):
    """
    Generates a v4 signed URL for uploading a blob using HTTP PUT.
    """
    auth_request = requests.Request()
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    bucket.cors = [
        {
            "origin": settings.GCS_BUCKET_ALLOWED_ORIGINS,
            "responseHeader": ["Content-Type", "x-goog-resumable"],
            "method": ["PUT"],
            "maxAgeSeconds": 3600,
        }
    ]
    bucket.patch()
    blob = bucket.blob(blob_name)

    url = ""

    # Retrieve credentials from within the cloudrun environment using a try block
    try:  # pragma: nocover
        signing_credentials = compute_engine.IDTokenCredentials(auth_request, "")
        url = blob.generate_signed_url(
            version="v4",
            credentials=signing_credentials,
            expiration=datetime.timedelta(hours=1),
            method="PUT",
            content_type=content_type,
        )
    except (TransportError, NewConnectionError):
        url = blob.generate_signed_url(
            version="v4",
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
