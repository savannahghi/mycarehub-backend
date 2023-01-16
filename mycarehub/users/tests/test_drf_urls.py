import pytest
from django.urls import reverse
from faker import Faker
from model_bakery import baker
from rest_framework import status

from mycarehub.users.models import GenderChoices, User, UserTypes

fake = Faker()
pytestmark = pytest.mark.django_db


def test_user_list(user_with_all_permissions, client):
    client.force_login(user_with_all_permissions)
    url = reverse("api:users-general")

    response = client.get(
        url,
        content_type="application/json",
        accept="application/json",
    )

    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    assert len(response_data) > 0


def test_user_registration(user_with_all_permissions, client):
    client.force_login(user_with_all_permissions)
    url = reverse("api:users-general")
    org = user_with_all_permissions.organisation
    program = user_with_all_permissions.program

    response = client.post(
        url,
        data={
            "user_id": fake.uuid4(),
            "name": fake.name(),
            "username": fake.name(),
            "user_type": UserTypes.CLIENT,
            "organisation_id": org.id,
            "program_id": program.id,
            "gender": GenderChoices.MALE,
            "date_of_birth": fake.date_of_birth(minimum_age=18),
        },
        content_type="application/json",
        accept="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED

    response_data = response.json()
    assert response_data["id"] is not None


def test_user_registration_invalid_input(user_with_all_permissions, client):
    client.force_login(user_with_all_permissions)
    url = reverse("api:users-general")

    response = client.post(
        url,
        data={
            "user_id": fake.uuid4(),
            "name": fake.name(),
            "username": fake.name(),
            "user_type": UserTypes.CLIENT,
            "gender": GenderChoices.MALE,
            "date_of_birth": fake.date_of_birth(minimum_age=18),
        },
        content_type="application/json",
        accept="application/json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_user_remove(user_with_all_permissions, client):
    client.force_login(user_with_all_permissions)
    user = baker.make(User)
    url = reverse("api:users-detail", kwargs={"pk": user.pk})
    response = client.delete(
        url,
        content_type="application/json",
        accept="application/json",
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
