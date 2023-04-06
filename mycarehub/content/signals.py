from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils.text import slugify
from wagtail.models import Page, Site

from mycarehub.common.models import Program
from mycarehub.content.models import ContentBookmark, ContentItem, ContentLike
from mycarehub.home.models import HomePage

from .models import ContentItemIndexPage


@receiver(post_save, sender=Program)
def create_program_content_index_page(sender, instance, created, **kwargs):
    # this check prevents the signal from running on creation of the default program
    # it causes a problem that prevents the running of `createsuperuser`
    if settings.DEFAULT_PROGRAM_ID == str(instance.id) and created:
        return

    try:
        homepage = HomePage.objects.get(title="SIL Home Page")
    except ObjectDoesNotExist:
        homepage_content_type = ContentType.objects.get_for_model(HomePage)

        homepage = HomePage(
            title="SIL Home Page",
            content_type=homepage_content_type,
        )
        homepage.slug = slugify(homepage.title)

        root = Page.get_first_root_node()
        root.add_child(instance=homepage)

        Site.objects.update_or_create(
            hostname="localhost",
            defaults={
                "root_page": homepage,
                "is_default_site": True,
                "site_name": "savannahinformatics.com",
            },
        )

    try:
        content_item_index = ContentItemIndexPage.objects.get(program=instance)
    except ObjectDoesNotExist:
        content_item_index = ContentItemIndexPage(
            title=f"{instance.name} Program Content",
            intro=f"Content for {instance.name} program",
            organisation=instance.organisation,
            program=instance,
        )

        homepage.add_child(instance=content_item_index)

        return

    content_item_index.organisation = instance.organisation
    content_item_index.program = instance

    content_item_index.save()


@receiver(post_delete, sender=ContentLike)
def reduce_like_count(sender, instance, *args, **kwargs):
    ContentItem.objects.filter(id=instance.content_item.id).update(like_count=F("like_count") - 1)


@receiver(post_delete, sender=ContentBookmark)
def reduce_bookmark_count(sender, instance, *args, **kwargs):
    ContentItem.objects.filter(id=instance.content_item.id).update(
        bookmark_count=F("bookmark_count") - 1
    )
