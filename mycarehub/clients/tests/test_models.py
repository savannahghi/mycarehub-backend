import pytest
from model_bakery import baker

from mycarehub.clients.models import Client

pytestmark = pytest.mark.django_db


def test_client_str(user_with_all_permissions):
    client = baker.make(Client, user=user_with_all_permissions, client_types=["PMTCT"])
    assert str(client) == f"{user_with_all_permissions.name} (['PMTCT'])"
