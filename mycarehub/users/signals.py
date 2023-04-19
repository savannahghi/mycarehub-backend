import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

LOGGER = logging.getLogger(__name__)
BASIC_PERMISSIONS = [
    "users.can_view_dashboard",
    "users.can_view_about",
]
WHITELIST_PERMISSIONS = BASIC_PERMISSIONS + [
    "common.view_facility",
]

User = get_user_model()


def assign_basic_permissions(user):
    for perm_string in BASIC_PERMISSIONS:
        content_type_app_label, perm_code_name = perm_string.split(".")
        perm = Permission.objects.get(
            content_type__app_label=content_type_app_label, codename=perm_code_name
        )
        user.user_permissions.add(perm)

    user.save()


def assign_whitelist_permissions(user):
    for perm_string in WHITELIST_PERMISSIONS:
        content_type_app_label, perm_code_name = perm_string.split(".")
        perm = Permission.objects.get(
            content_type__app_label=content_type_app_label, codename=perm_code_name
        )
        user.user_permissions.add(perm)

    user.save()


def is_from_whitelist_domain(user_email):
    email = user_email.strip().lower()
    for domain in settings.WHITELISTED_DOMAINS:
        if email.endswith(domain):
            return True

    return False


@receiver(post_save, sender=User)
def account_confirmed_handler(sender, instance, created, **kwargs):
    if created:
        assign_basic_permissions(instance)
        if is_from_whitelist_domain(instance.email):
            assign_whitelist_permissions(instance)
            instance.save()

        return

    return True


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def assign_user_editor_permission(sender, instance, created, **kwargs):
    try:
        group = Group.objects.get(name=f"{instance.program.name} Editor")
    except ObjectDoesNotExist:
        return

    instance.groups.clear()
    instance.groups.add(group)
