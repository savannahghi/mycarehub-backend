import pytest
from django.urls import reverse
from faker import Faker
from model_bakery import baker
from rest_framework import status

from mycarehub.authority.models import AuthorityRole
from mycarehub.common.models.common_models import Facility

fake = Faker()
pytestmark = pytest.mark.django_db


def test_staff_registration_view_valid(user_with_all_permissions, client):
    client.force_login(user_with_all_permissions)
    url = reverse("staff_registration")
    org = user_with_all_permissions.organisation
    facility = baker.make(Facility, organisation=org)
    role = baker.make(AuthorityRole, organisation=org)
    response = client.post(
        url,
        data={
            "facility": facility.name,
            "name": fake.name(),
            "gender": "MALE",
            "date_of_birth": fake.date_of_birth(minimum_age=18),
            "phone_number": "+254722000000",
            "id_number": fake.random_int(),
            "staff_number": fake.random_int(),
            "role": role.name,
        },
        content_type="application/json",
        accept="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED

    response_data = response.json()
    assert response_data["id"] is not None


def test_staff_registration_view_invalid(user_with_all_permissions, client):
    client.force_login(user_with_all_permissions)
    url = reverse("staff_registration")
    response = client.post(
        url,
        data={},
        content_type="application/json",
        accept="application/json",
    )
    assert response.status_code == 400


def test_staff_registration_serializer_invalid(user_with_all_permissions, client):
    client.force_login(user_with_all_permissions)
    url = reverse("staff_registration")
    response = client.post(
        url,
        data={
            "facility": "bonkers",
        },
        content_type="application/json",
        accept="application/json",
    )
    assert response.status_code == 400
