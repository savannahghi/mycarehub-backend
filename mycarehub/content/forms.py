from django.core.files.storage import get_storage_class
from wagtailmedia.forms import BaseMediaForm

from mycarehub.utils.signed_url import generate_media_name


class CustomBaseMediaForm(BaseMediaForm):
    def save(self, commit=True):  # pragma: nocover
        instance = super().save(commit=False)

        # Checks the storage class being used
        # Google Cloud Storage should save only the file name
        # because the upload is already done using a signed url
        if get_storage_class().__name__ == "MediaRootGoogleCloudStorage":  # pragma: nocover
            temp_file = instance.file
            instance.file = generate_media_name(temp_file.name)

        if commit:
            instance.save()

        return instance
