import random
import uuid

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from faker import Faker
from model_bakery import baker

from mycarehub.common.models.common_models import Facility
from mycarehub.common.tests.test_api import CRUDTestMixin

from .models import (
    Client,
    ClientFacility,
    Identifier,
    RelatedPerson,
    SecurityQuestion,
    SecurityQuestionResponse,
)

fake = Faker()


class IdentifierViewsetTest(CRUDTestMixin):
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


class SecurityQuestionViewsetTest(CRUDTestMixin):
    def setUp(self):
        self.url_list = reverse("api:securityquestion-list")
        self.comparison_field = "stem"
        self.url_detail_base = "api:securityquestion-detail"
        self.instance = baker.make(
            SecurityQuestion,
            stem=fake.text(),
            description=fake.text(),
            organisation=self.global_organisation,
        )
        self.data = {
            "identifier_type": "NATIONAL_ID",
            "stem": fake.text(),
            "description": fake.text(),
            "sequence": random.randint(1, 999_999),
            "response_type": "TEXT",
            "organisation": self.global_organisation.pk,
        }
        self.detail_url = reverse(self.url_detail_base, kwargs={"pk": self.instance.pk})
        super().setUp()


class SecurityQuestionResponseViewsetTest(CRUDTestMixin):
    def setUp(self):
        super().setUp()  # comes early because we need the user
        self.url_list = reverse("api:securityquestionresponse-list")
        self.comparison_field = "response"
        self.url_detail_base = "api:securityquestionresponse-detail"
        self.question = baker.make(
            SecurityQuestion,
            stem=fake.text(),
            description=fake.text(),
            organisation=self.global_organisation,
        )
        self.instance = baker.make(
            SecurityQuestionResponse,
            question=self.question,
            user=self.user,
            organisation=self.global_organisation,
        )

        # we need another user because of a uniqueness constraint
        another_user = get_user_model().objects.create_superuser(
            email=fake.email(),
            password="pass123",
            username=str(uuid.uuid4()),
        )
        self.data = {
            "user": str(another_user.pk),
            "question": self.question.pk,
            "timestamp": timezone.now().isoformat(),
            "response": fake.text(),
            "organisation": self.global_organisation.pk,
        }
        self.detail_url = reverse(self.url_detail_base, kwargs={"pk": self.instance.pk})


class RelatedPersonViewsetTest(CRUDTestMixin):
    def setUp(self):
        self.url_list = reverse("api:relatedperson-list")
        self.comparison_field = "first_name"
        self.url_detail_base = "api:relatedperson-detail"
        self.instance = baker.make(
            RelatedPerson,
            organisation=self.global_organisation,
        )
        self.data = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "other_name": fake.name(),
            "date_of_birth": fake.date_of_birth().isoformat(),
            "gender": "FEMALE",
            "relationship_type": "SPOUSE",
            "organisation": self.global_organisation.pk,
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
        identifier = baker.make(
            Identifier,
            identifier_type="NATIONAL_ID",
            identifier_value=fake.ssn(),
            identifier_use="OFFICIAL",
            description=fake.text(),
            is_primary_identifier=True,
            organisation=self.global_organisation,
        )

        self.instance = baker.make(
            Client,
            client_type="PMTCT",
            user=self.user,
            current_facility=facility,
            fhir_patient_id=str(uuid.uuid4()),
            organisation=self.global_organisation,
        )
        self.instance.identifiers.add(identifier)
        self.instance.save()

        another_user = get_user_model().objects.create_superuser(
            email=fake.email(),
            password="pass123",
            username=str(uuid.uuid4()),
        )
        self.data = {
            "client_type": "PMTCT",
            "user": str(another_user.pk),
            "current_facility": str(facility.pk),
            "fhir_patient_id": str(uuid.uuid4()),
            "identifiers": [str(identifier.pk)],
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
        identifier = baker.make(
            Identifier,
            identifier_type="NATIONAL_ID",
            identifier_value=fake.ssn(),
            identifier_use="OFFICIAL",
            description=fake.text(),
            is_primary_identifier=True,
            organisation=self.global_organisation,
        )

        client = baker.make(
            Client,
            client_type="PMTCT",
            user=self.user,
            current_facility=facility,
            fhir_patient_id=str(uuid.uuid4()),
            organisation=self.global_organisation,
        )
        client.identifiers.add(identifier)
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
            client_type="PMTCT",
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
