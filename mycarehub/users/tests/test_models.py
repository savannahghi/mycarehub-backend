import pytest

from mycarehub.users.models import User
from mycarehub.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_user_get_absolute_url(user: User):
    assert user.get_absolute_url() == f"/users/{user.username}/"


def test_user_permissions_with_permissions(user_with_all_permissions):
    assert len(user_with_all_permissions.permissions) > 2


def test_user_permissions_with_permissions_via_groups(user_with_group):
    assert len(user_with_group.permissions) > 2


def test_user_groups_no_groups(user):
    assert user.gps == "-"


def test_user_groups_with_groups(user_with_group):
    assert len(user_with_group.gps) > 2


def test_user_string_representation(program):
    user1 = UserFactory(username="admin", name="Juha Kalulu", program=program)
    user2 = UserFactory(username="anonymous_weasel", name="", program=program)
    user3 = UserFactory(program=program)

    assert str(user1) == "Juha Kalulu (admin)"
    assert str(user2) == "anonymous_weasel"
    assert str(user3) == "{} ({})".format(user3.name, user3.username)
