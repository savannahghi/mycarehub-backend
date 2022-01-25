import pytest
from model_bakery import baker

from mycarehub.staff.models import Staff

pytestmark = pytest.mark.django_db


def test_staff_str(user_with_all_permissions):
    staff = baker.make(Staff, user=user_with_all_permissions, staff_number="s123456")
    assert str(staff) == "s123456"
