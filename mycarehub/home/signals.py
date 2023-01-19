from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver
from wagtail.models import Page

from mycarehub.common.models import Organisation
from mycarehub.home.models import HomePage


@receiver(post_save, sender=Organisation)
def create_organisation_home_page(sender, instance, created, **kwargs):
    if created:
        root = Page.get_first_root_node()

        homepage_content_type = ContentType.objects.get_for_model(HomePage)

        homepage = HomePage(
            title=f"{instance.organisation_name} Home",
            content_type=homepage_content_type,
            organisation=instance,
        )

        root.add_child(instance=homepage)
