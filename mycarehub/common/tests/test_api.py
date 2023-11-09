"""Test for the common views."""
import shutil
import uuid
from functools import partial
from os import path

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.urls import reverse
from faker import Faker
from model_bakery import baker
from model_bakery.recipe import Recipe
from rest_framework import status
from rest_framework.test import APITestCase

from mycarehub.common.constants import WHITELIST_COUNTIES
from mycarehub.common.models import Facility, Organisation, Program, UserFacilityAllotment

DIR_PATH = path.join(path.dirname(path.abspath(__file__)))
MEDIA_PATH = path.join(DIR_PATH, "media")

pytestmark = pytest.mark.django_db


http_origin_header = {"HTTP_ORIGIN": "http://sil.com"}
fake = Faker()


def delete_media_file():
    """Delete the media folder after tests."""
    if path.exists(MEDIA_PATH):
        shutil.rmtree(MEDIA_PATH)


def global_organisation():
    """Create organisation for running test."""
    org_id = "ebef581c-494b-4772-9e49-0b0755c44e61"
    code = 50
    name = "Demo Hospital"
    try:
        return Organisation.objects.get(
            id=org_id,
            code=code,
            name=name,
        )
    except Organisation.DoesNotExist:
        return baker.make(
            Organisation,
            id=org_id,
            name=name,
            code=code,
        )


class LoggedInMixin(APITestCase):
    """Define a logged in session for use in tests."""

    def setUp(self):
        """Create a test user for the logged in session."""
        super(LoggedInMixin, self).setUp()
        username = str(uuid.uuid4())
        self.program = baker.make(Program)
        self.user = get_user_model().objects.create_superuser(
            email=fake.email(), password="pass123", username=username, program=self.program
        )
        all_perms = Permission.objects.all()
        for perm in all_perms:
            self.user.user_permissions.add(perm)
        self.user.organisation = self.global_organisation
        self.user.save()

        # Allot the given users to all the facilities in FYJ counties
        self.user_facility_allotment = baker.make(
            UserFacilityAllotment,
            allotment_type=UserFacilityAllotment.AllotmentType.BY_REGION.value,
            counties=WHITELIST_COUNTIES,
            organisation=self.global_organisation,
            region_type=UserFacilityAllotment.RegionType.COUNTY.value,
            user=self.user,
        )

        assert self.client.login(username=username, password="pass123") is True

        headers = self.extra_headers()
        self.client.get = partial(self.client.get, **headers)
        self.client.patch = partial(self.client.patch, **headers)
        self.client.post = partial(self.client.post, **headers)

    @property
    def global_organisation(self):
        """Create test organisation for the user."""
        return global_organisation()

    def make_recipe(self, model, **kwargs):
        """Ensure test user part of an organisation."""
        if "organisation" not in kwargs:
            kwargs["organisation"] = self.user.organisation
        return Recipe(model, **kwargs)

    def extra_headers(self):
        """Return an empty headers list."""
        return {}


def test_organisation_registration(user_with_all_permissions, client):
    client.force_login(user_with_all_permissions)
    url = reverse("api:organisations-general")

    response = client.post(
        url,
        data={
            "organisation_id": fake.uuid4(),
            "name": fake.name(),
            "code": fake.random_int(min=100),
            "phone_number": "+254722000000",
            "email": fake.email(),
        },
        content_type="application/json",
        accept="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED

    response_data = response.json()
    assert response_data["id"] is not None


def test_organisation_registration_invalid_input(user_with_all_permissions, client):
    client.force_login(user_with_all_permissions)
    url = reverse("api:organisations-general")

    response = client.post(
        url,
        data={
            "organisation_id": fake.uuid4(),
            "name": fake.name(),
        },
        content_type="application/json",
        accept="application/json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_program_registration(user_with_all_permissions, client):
    client.force_login(user_with_all_permissions)
    url = reverse("api:programs-general")

    response = client.post(
        url,
        data={
            "program_id": fake.uuid4(),
            "name": fake.name(),
            "organisation_id": user_with_all_permissions.organisation.id,
        },
        content_type="application/json",
        accept="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED

    response_data = response.json()
    assert response_data["id"] is not None


def test_program_list(user_with_all_permissions, client):
    client.force_login(user_with_all_permissions)
    url = reverse("api:programs-general")

    response = client.get(
        url,
        content_type="application/json",
        accept="application/json",
    )

    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    assert response_data[0]["id"] is not None


def test_program_registration_invalid_input(user_with_all_permissions, client):
    client.force_login(user_with_all_permissions)
    url = reverse("api:programs-general")

    response = client.post(
        url,
        data={
            "program_id": fake.uuid4(),
        },
        content_type="application/json",
        accept="application/json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_program_patch_no_facilities(user_with_all_permissions, client):
    program = baker.make(Program)

    client.force_login(user_with_all_permissions)
    url = reverse("api:programs-detail", kwargs={"pk": program.id})

    response = client.patch(
        url,
        data={
            "name": fake.name(),
        },
        content_type="application/json",
        accept="application/json",
    )

    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    assert response_data["id"] == str(program.id)


def test_program_patch_facilities(user_with_all_permissions, client):
    program = baker.make(Program)

    client.force_login(user_with_all_permissions)
    url = reverse("api:programs-detail", kwargs={"pk": program.id})

    facility = baker.make(Facility)

    response = client.patch(
        url,
        data={
            "name": fake.name(),
            "facilities": [facility.id],
        },
        content_type="application/json",
        accept="application/json",
    )

    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    assert response_data["id"] == str(program.id)


def test_program_patch_invalid_data(user_with_all_permissions, client):
    program = baker.make(Program)

    client.force_login(user_with_all_permissions)
    url = reverse("api:programs-detail", kwargs={"pk": program.id})

    response = client.patch(
        url,
        data={
            "name": 12123123,
            "facilities": ["invalid"],
        },
        content_type="application/json",
        accept="application/json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_list_facilities(user_with_all_permissions, client):
    baker.make(Facility, _quantity=10, organisation=user_with_all_permissions.organisation)

    client.force_login(user_with_all_permissions)
    url = reverse("api:facility-list")

    response = client.get(
        url,
        content_type="application/json",
        accept="application/json",
    )

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["count"] == 10

    response_two = client.post(
        url,
        data={
            "name": fake.name(),
            "mfl_code": fake.random_int(min=100),
        },
        content_type="application/json",
        accept="application/json",
    )

    assert response_two.status_code == status.HTTP_201_CREATED
    response_data = response_two.json()
    assert response_data["id"] is not None

    response = client.get(
        url,
        content_type="application/json",
        accept="application/json",
    )

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["count"] == 11


def test_create_facility(user_with_all_permissions, client):
    client.force_login(user_with_all_permissions)
    url = reverse("api:facility-list")

    response = client.post(
        url,
        data={
            "name": fake.name(),
            "mfl_code": fake.random_int(min=100),
            "organisation": str(fake.uuid4()),
        },
        content_type="application/json",
        accept="application/json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    org = baker.make(Organisation)
    response = client.post(
        url,
        data={
            "name": "Test Facility",
            "mfl_code": fake.random_int(min=100),
            "organisation": str(org.id),
        },
        content_type="application/json",
        accept="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED

    response_data = response.json()
    assert response_data["id"] is not None
    assert response_data["name"] == "Test Facility"
