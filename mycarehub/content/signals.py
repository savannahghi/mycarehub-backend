from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver

from mycarehub.common.models import Program
from mycarehub.home.models import HomePage

from .models import ContentItemIndexPage


@receiver(post_save, sender=Program)
def create_program_content_index_page(sender, instance, created, **kwargs):
    if created:
        try:
            homepage = HomePage.objects.get(organisation=instance.organisation)
        except ObjectDoesNotExist:
            print("none")
            return

        content_item_index = ContentItemIndexPage(
            title=f"{instance.name} Program Content",
            intro=f"Content for {instance.name} program",
            organisation=instance.organisation,
            program=instance,
        )

        homepage.add_child(instance=content_item_index)
