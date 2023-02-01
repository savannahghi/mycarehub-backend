from django.core.files.storage import get_storage_class
from wagtail.documents.forms import BaseDocumentForm
from wagtail.images.forms import BaseImageForm
from wagtailmedia.forms import BaseMediaForm

from mycarehub.utils.signed_url import generate_media_name


class CustomBaseMediaForm(BaseMediaForm):
    def __init__(self, *args, **kwargs):  # pragma: no cover
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.instance.organisation = kwargs["user"].organisation

    def save(self, commit=True):  # pragma: no cover
        instance = super().save(commit=False)

        # Checks the storage class being used
        # Google Cloud Storage should save only the file name
        # because the upload is already done using a signed url
        if get_storage_class().__name__ == "MediaRootGoogleCloudStorage":  # pragma: no cover
            temp_file = instance.file
            instance.file = generate_media_name(temp_file.name)

        if commit:
            instance.save()

        return instance


class CustomImageForm(BaseImageForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.instance.organisation = kwargs["user"].organisation


class CustomDocumentForm(BaseDocumentForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.instance.organisation = kwargs["user"].organisation
