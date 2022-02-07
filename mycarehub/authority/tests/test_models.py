import pytest
from model_bakery import baker

from mycarehub.authority.models import AuthorityPermission, AuthorityRole

pytestmark = pytest.mark.django_db


def test_authority_permission():
    permissions = baker.make(AuthorityPermission, name="CAN_EDIT_USER")
    assert str(permissions) == "CAN_EDIT_USER"


def test_authority_roles(user_with_all_permissions):
    permission = baker.make(AuthorityPermission, name="CAN_EDIT_USER")
    user = user_with_all_permissions
    roles = baker.make(AuthorityRole, users=[user], name="SYSTEM_ADMIN", permissions=[permission])
    assert str(roles) == "SYSTEM_ADMIN"
