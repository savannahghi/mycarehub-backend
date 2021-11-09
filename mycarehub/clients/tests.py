from django.urls import reverse
from faker import Faker
from model_bakery import baker
from rest_framework.test import APITestCase

from mycarehub.common.tests.test_api import LoggedInMixin

from .models import Identifier

fake = Faker()


class IdentifierViewsetTest(LoggedInMixin, APITestCase):
    def setUp(self):
        self.url_list = reverse("api:identifier-list")
        self.comparison_field = "identifier_value"
        self.url_detail_base = "api:identifier-detail"
        self.instance = baker.make(
            Identifier,
            identifier_type="NATIONAL_ID",
            identifier_value=fake.ssn(),
            identifier_use="OFFICIAL",
            description=fake.text(),
            is_primary_identifier=True,
            organisation=self.global_organisation,
        )
        self.data = {
            "identifier_type": "NATIONAL_ID",
            "identifier_value": fake.ssn(),
            "identifier_use": "OFFICIAL",
            "description": fake.text(),
            "is_primary_identifier": True,
            "organisation": self.global_organisation.pk,
        }
        self.detail_url = reverse(self.url_detail_base, kwargs={"pk": self.instance.pk})
        super().setUp()

    def test_create(self):
        response = self.client.post(self.url_list, self.data)
        assert response.status_code == 201, response.json()
        assert response.data[self.comparison_field] == self.data[self.comparison_field]

    def test_list(self):
        response = self.client.get(self.url_list)
        assert response.status_code == 200, response.json()
        assert response.data["count"] >= 1, response.json()

        values = [a[self.comparison_field] for a in response.data["results"]]
        assert getattr(self.instance, self.comparison_field) in values

    def test_retrieve(self):
        response = self.client.get(self.detail_url)
        assert response.status_code == 200, response.json()
        assert response.data[self.comparison_field] == getattr(
            self.instance, self.comparison_field
        )

    def test_patch(self):
        patch = {self.comparison_field: fake.ssn()}
        response = self.client.patch(self.detail_url, patch)
        assert response.status_code == 200, response.json()
        assert response.data[self.comparison_field] == patch[self.comparison_field]

    def test_put(self):
        response = self.client.put(self.detail_url, self.data)
        assert response.status_code == 200, response.json()
        assert response.data[self.comparison_field] == self.data[self.comparison_field]
