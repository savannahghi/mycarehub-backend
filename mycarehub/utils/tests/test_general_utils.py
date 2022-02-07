import pytest

from ..general_utils import default_organisation

pytestmark = pytest.mark.django_db


def test_default_organisation():
    first_fetch_org = default_organisation()
    second_fetch_org = default_organisation()
    assert str(first_fetch_org) == str(second_fetch_org)
