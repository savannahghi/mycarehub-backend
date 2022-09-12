import uuid

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from faker import Faker
from model_bakery import baker
from rest_framework import status

from mycarehub.common.models.common_models import Facility
from mycarehub.staff.models import Staff

fake = Faker()
pytestmark = pytest.mark.django_db


def test_staff_registration_view_valid(user_with_all_permissions, client):
    client.force_login(user_with_all_permissions)
    url = reverse("staff_registration")
    org = user_with_all_permissions.organisation
    facility = baker.make(Facility, organisation=org)
    response = client.post(
        url,
        data={
            "user_id": fake.uuid4(),
            "handle": fake.name(),
            "organisation_id": org.id,
            "facility_id": facility.id,
            "facility_name": facility.name,
            "name": fake.name(),
            "gender": "MALE",
            "date_of_birth": fake.date_of_birth(minimum_age=18),
            "phone_number": "+254722000000",
            "staff_id": fake.uuid4(),
            "staff_number": fake.random_int(),
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


def test_staff_deletion_view_valid(user_with_all_permissions, client):
    client.force_login(user_with_all_permissions)
    org = user_with_all_permissions.organisation

    facility = baker.make(Facility, organisation=org)
    facility_two = baker.make(Facility, organisation=org)
    user = get_user_model().objects.create_superuser(
        email=fake.email(),
        password="pass123",
        username=str(uuid.uuid4()),
    )

    staff = baker.make(
        Staff,
        user=user,
        default_facility=facility,
        staff_number=fake.name(),
    )

    staff.facilities.add(facility)
    staff.facilities.add(facility_two)

    staff.save()

    url = reverse("staff_removal", kwargs={"pk": user.id})

    response = client.delete(
        url,
        content_type="application/json",
        accept="application/json",
    )

    assert response.status_code == 200


def test_staff_deletion_view_invalid(user_with_all_permissions, client):
    client.force_login(user_with_all_permissions)

    user = get_user_model().objects.create_superuser(
        email=fake.email(),
        password="pass123",
        username=str(uuid.uuid4()),
    )

    url = reverse("staff_removal", kwargs={"pk": user.id})

    response = client.delete(
        url,
        content_type="application/json",
        accept="application/json",
    )

    assert response.status_code == 400
