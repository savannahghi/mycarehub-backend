import uuid

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from faker import Faker
from model_bakery import baker
from rest_framework import status

from mycarehub.clients.models import Caregiver, Client, ClientFacility
from mycarehub.common.models.common_models import Facility
from mycarehub.common.tests.test_api import CRUDTestMixin

fake = Faker()

pytestmark = pytest.mark.django_db


class CaregiverViewsetTest(CRUDTestMixin):
    def setUp(self):
        self.url_list = reverse("api:caregiver-list")
        self.comparison_field = "first_name"
        self.url_detail_base = "api:caregiver-detail"
        self.instance = baker.make(
            Caregiver,
            organisation=self.global_organisation,
        )
        self.data = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "caregiver_type": "FATHER",
            "phone_number": fake.phone_number(),
        }
        self.detail_url = reverse(self.url_detail_base, kwargs={"pk": self.instance.pk})
        super().setUp()


class ClientViewsetTest(CRUDTestMixin):
    def setUp(self):
        super().setUp()  # early, because we need the user initialized
        self.url_list = reverse("api:client-list")
        self.comparison_field = "fhir_patient_id"
        self.url_detail_base = "api:client-detail"

        facility = baker.make(
            Facility,
            organisation=self.global_organisation,
        )

        self.instance = baker.make(
            Client,
            client_types=["PMTCT"],
            user=self.user,
            current_facility=facility,
            fhir_patient_id=str(uuid.uuid4()),
            organisation=self.global_organisation,
        )
        self.instance.save()

        another_user = get_user_model().objects.create_superuser(
            email=fake.email(),
            password="pass123",
            username=str(uuid.uuid4()),
        )
        self.data = {
            "client_types": ["PMTCT"],
            "user": str(another_user.pk),
            "current_facility": str(facility.pk),
            "fhir_patient_id": str(uuid.uuid4()),
            "organisation": self.global_organisation.pk,
        }
        self.detail_url = reverse(self.url_detail_base, kwargs={"pk": self.instance.pk})


class ClientFacilityViewsetTest(CRUDTestMixin):
    def setUp(self):
        super().setUp()  # early, because we need the user initialized
        self.url_list = reverse("api:clientfacility-list")
        self.comparison_field = "notes"
        self.url_detail_base = "api:clientfacility-detail"

        facility = baker.make(
            Facility,
            organisation=self.global_organisation,
        )

        client = baker.make(
            Client,
            client_types=["PMTCT"],
            user=self.user,
            current_facility=facility,
            fhir_patient_id=str(uuid.uuid4()),
            organisation=self.global_organisation,
        )
        client.save()

        self.instance = baker.make(
            ClientFacility,
            client=client,
            facility=facility,
            notes=fake.text(),
        )

        another_user = get_user_model().objects.create_superuser(
            email=fake.email(),
            password="pass123",
            username=str(uuid.uuid4()),
        )
        another_client = baker.make(
            Client,
            client_types=["PMTCT"],
            user=another_user,
            current_facility=facility,
            fhir_patient_id=str(uuid.uuid4()),
            organisation=self.global_organisation,
        )
        another_facility = baker.make(
            Facility,
            organisation=self.global_organisation,
        )
        self.data = {
            "client": str(another_client.pk),
            "facility": str(another_facility.pk),
            "notes": fake.text(),
            "organisation": self.global_organisation.pk,
        }
        self.detail_url = reverse(self.url_detail_base, kwargs={"pk": self.instance.pk})


def test_client_registration_view_valid(user_with_all_permissions, client):
    client.force_login(user_with_all_permissions)
    url = reverse("client_registration")
    org = user_with_all_permissions.organisation
    facility = baker.make(Facility, organisation=org)
    response = client.post(
        url,
        data={
            "user_id": fake.uuid4(),
            "handle": fake.name(),
            "facility_id": facility.id,
            "organisation_id": org.id,
            "facility_name": facility.name,
            "client_id": fake.uuid4(),
            "client_types": ["PMTCT"],
            "name": fake.name(),
            "gender": "MALE",
            "date_of_birth": fake.date_of_birth(minimum_age=5),
            "phone_number": "+254722000000",
            "enrollment_date": fake.date_this_century(),
        },
        content_type="application/json",
        accept="application/json",
    )

    print(response.content)
    assert response.status_code == status.HTTP_201_CREATED

    response_data = response.json()
    assert response_data["id"] is not None


def test_client_registration_view_invalid(user_with_all_permissions, client):
    client.force_login(user_with_all_permissions)
    url = reverse("client_registration")
    response = client.post(
        url,
        data={},  # blank, invalid by default
        content_type="application/json",
        accept="application/json",
    )
    assert response.status_code == 400
