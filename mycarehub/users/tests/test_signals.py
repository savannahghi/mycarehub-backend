import pytest
from django.contrib.auth import get_user_model
from faker import Faker
from model_bakery import baker
from rest_framework.authtoken.models import Token

from mycarehub.users.signals import (
    BASIC_PERMISSIONS,
    account_confirmed_handler,
    assign_basic_permissions,
    is_from_whitelist_domain,
)

pytestmark = pytest.mark.django_db

User = get_user_model()
fake = Faker()


def test_account_confirmed_handler_newly_created(program):
    user = baker.make(
        User,
        email=fake.email(),
        program=program,
    )
    assert account_confirmed_handler(User, user, created=True) is None


def test_assign_basic_permission(program):
    user = baker.make(User, email=fake.email(), program=program)
    assign_basic_permissions(user)
    perms = user.get_user_permissions()
    assert len(perms) == len(BASIC_PERMISSIONS)
    for perm in BASIC_PERMISSIONS:
        assert user.has_perm(perm)


def test_is_from_whitelist_domain():
    assert is_from_whitelist_domain("ngure@savannahghi.org") is True
    assert is_from_whitelist_domain("kalulu@juha.com") is False


def test_account_confirmed_handler_newly_created_whitelist_user(program):
    user = baker.make(
        User,
        email="noreply@savannahghi.org",
        program=program,
    )
    assert account_confirmed_handler(User, user, created=True) is None


def test_create_auth_token(program):
    # create a user
    user = baker.make(
        User,
        email="token@savannahghi.org",
        program=program,
    )

    # confirm that a token was created
    token = Token.objects.get(user=user)
    assert token is not None

    # update the user
    user.email = "token2@savannahghi.org"
    user.save()

    # re-fetch the token
    token2 = Token.objects.get(user__email="token2@savannahghi.org")
    assert token2 is not None

    # confirm that the token was not regenerated
    assert token.pk == token2.pk
