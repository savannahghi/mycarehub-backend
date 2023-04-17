from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from wagtail.documents.models import Document
from wagtail.images.models import Image
from wagtail.models import Collection, GroupCollectionPermission, GroupPagePermission, Page, Site
from wagtailmedia.models import Media

from mycarehub.common.models import Program
from mycarehub.content.models import (
    Author,
    ContentBookmark,
    ContentItem,
    ContentItemCategory,
    ContentLike,
)
from mycarehub.home.models import HomePage

from .models import ContentItemIndexPage


@receiver(post_save, sender=Program)
def create_program_content_index_page(sender, instance, created, **kwargs):
    # this check prevents the signal from running on creation of the default program
    # it causes a problem that prevents the running of `createsuperuser`
    if settings.DEFAULT_PROGRAM_ID == str(instance.id) and created:
        return

    try:
        homepage = HomePage.objects.get(title="Mycarehub Home Page")
    except ObjectDoesNotExist:
        homepage_content_type = ContentType.objects.get_for_model(HomePage)

        homepage = HomePage(
            title="Mycarehub Home Page",
            content_type=homepage_content_type,
        )

        root = Page.get_first_root_node()
        root.add_child(instance=homepage)

        Site.objects.update_or_create(
            hostname="localhost",
            defaults={
                "root_page": homepage,
                "is_default_site": True,
                "site_name": "mycarehub.com",
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


# receiver that runs after creation of content item index page
@receiver(post_save, sender=ContentItemIndexPage)
def create_program_content_editor_permissions(sender, instance, created, **kwargs):
    group = Group.objects.create(name=f"{instance.program.name} Editor")

    can_access_wagtail_admin = Permission.objects.get(
        content_type=ContentType.objects.get(app_label="wagtailadmin", model="admin"),
        codename="access_admin",
    )
    group.permissions.add(can_access_wagtail_admin)

    allowed_author_permissions = ["add_author", "change_author"]
    for permission in allowed_author_permissions:
        permission_object = Permission.objects.get(
            content_type=ContentType.objects.get_for_model(Author), codename=permission
        )
        group.permissions.add(permission_object)

    allowed_content_category_permissions = [
        "add_contentitemcategory",
        "change_contentitemcategory",
    ]
    for permission in allowed_content_category_permissions:
        permission_object = Permission.objects.get(
            content_type=ContentType.objects.get_for_model(ContentItemCategory),
            codename=permission,
        )
        group.permissions.add(permission_object)

    allowed_page_permissions = ["add", "edit", "publish"]
    for permission in allowed_page_permissions:
        GroupPagePermission.objects.create(group=group, page=instance, permission_type=permission)

    root_collection = Collection.get_first_root_node()
    allowed_image_permissions = ["add_image", "choose_image", "change_image", "delete_image"]
    for permission in allowed_image_permissions:
        GroupCollectionPermission.objects.create(
            group=group,
            collection=root_collection,
            permission=Permission.objects.get(
                content_type=ContentType.objects.get_for_model(Image), codename=permission
            ),
        )

    allowed_document_permissions = [
        "add_document",
        "choose_document",
        "change_document",
        "delete_document",
    ]

    for permission in allowed_document_permissions:
        GroupCollectionPermission.objects.create(
            group=group,
            collection=root_collection,
            permission=Permission.objects.get(
                content_type=ContentType.objects.get_for_model(Document), codename=permission
            ),
        )

    allowed_media_permissions = ["add_media", "delete_media", "change_media"]

    for permission in allowed_media_permissions:
        GroupCollectionPermission.objects.create(
            group=group,
            collection=root_collection,
            permission=Permission.objects.get(
                content_type=ContentType.objects.get_for_model(Media), codename=permission
            ),
        )


@receiver(post_delete, sender=ContentLike)
def reduce_like_count(sender, instance, *args, **kwargs):
    ContentItem.objects.filter(id=instance.content_item.id).update(like_count=F("like_count") - 1)


@receiver(post_delete, sender=ContentBookmark)
def reduce_bookmark_count(sender, instance, *args, **kwargs):
    ContentItem.objects.filter(id=instance.content_item.id).update(
        bookmark_count=F("bookmark_count") - 1
    )
