import datetime
import os
import uuid
from random import randint
from unittest.mock import patch

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from faker import Faker
from model_bakery import baker
from PIL import Image

from mycarehub.common.models import (
    Facility,
    Organisation,
    OwnerlessAbstractBase,
    Program,
    UserFacilityAllotment,
    is_image_type,
    unique_list,
)

fake = Faker()

pytestmark = pytest.mark.django_db

CURRENT_FOLDER = os.path.dirname(__file__)


def test_unique_list():
    """Test for getting the unique list."""
    lst = [1, 2, 2, 3]
    unique = unique_list(lst)
    assert unique == [1, 2, 3]


def test_is_image_type():
    assert is_image_type("image/png") is True
    assert is_image_type("image/jpeg") is True
    assert is_image_type("application/pdf") is False


def test_facility_string_representation():
    """Test common behavior of the abstract base model."""
    facility_name = fake.name()
    mfl_code = randint(1, 999_999)
    county = "Nairobi"
    created_by = uuid.uuid4()
    updated_by = created_by
    organisation = baker.make("common.Organisation")

    facility = Facility(
        name=facility_name,
        mfl_code=mfl_code,
        county=county,
        organisation=organisation,
        created_by=created_by,
        updated_by=updated_by,
    )
    facility.save()
    assert str(facility) == f"{facility_name}"


def test_google_application_credentials():
    cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
    assert cred_path != ""
    assert os.path.exists(cred_path)
    assert os.path.isfile(cred_path)


def get_temporary_image(temp_file):
    size = (200, 200)
    color = (255, 0, 0, 0)
    image = Image.new("RGB", size, color)
    image.save(temp_file, "jpeg")
    return temp_file


def test_facility_error_saving():
    """Test common behavior of the abstract base model."""
    facility_name = "a"  # too short, will trigger validator
    mfl_code = randint(1, 999_999)
    county = "Nairobi"
    created_by = uuid.uuid4()
    updated_by = created_by
    organisation = baker.make("common.Organisation")

    facility = Facility(
        name=facility_name,
        mfl_code=mfl_code,
        county=county,
        organisation=organisation,
        created_by=created_by,
        updated_by=updated_by,
    )
    with pytest.raises(ValidationError) as e:
        facility.save()

    assert "the facility name should exceed 3 characters" in e.value.messages


def test_organisation_string_representation():
    org = baker.make("common.Organisation", name="Test Organisation")
    assert str(org) == "Test Organisation"


def test_program_string_representation():
    program = baker.make("common.Program", name="Test Program")
    assert str(program) == "Test Program"


class DictError(OwnerlessAbstractBase):
    """Raise validation errors with a dict."""

    class Meta:
        """Define app name for the model."""

        app_label = "dict_error"

    model_validators = [
        "validation_one",
        "validation_two",
        "validation_three",
        "validation_four",
        "validation_one",  # duplicate
    ]

    def validation_one(self):
        """Define first validation raise with a dictionary."""
        raise ValidationError({"field_1": "Error!", "field_2": "Error!"})

    def validation_two(self):
        """Define second validation raise with a dictionary."""
        raise ValidationError({"field_1": "Error2!"})

    def validation_three(self):
        """Define third validation raise with a message."""
        raise ValidationError("plain error")

    def validation_four(self):
        """Define fourth validation raise with a list of messages."""
        raise ValidationError(["list error one", "list error two"])


def test_run_model_validators():
    """Test model validation."""
    instance = DictError()
    with pytest.raises(ValidationError) as e:
        instance.run_model_validators()

    assert e.value.message_dict == {
        "field_1": ["Error!", "Error2!"],
        "field_2": ["Error!"],
        "__all__": ["plain error", "list error one", "list error two"],
    }


def test_duplicate_validator_ignored():
    """Test same validator not run twice on a model."""
    instance = DictError()
    with patch.object(instance, "validation_one") as validation_one:
        with pytest.raises(ValidationError):
            instance.run_model_validators()

    validation_one.assert_called_once_with()


def test_abstract_base_manager_get_active():
    """Tests for AbstractBaseManager."""
    organisation = baker.make(Organisation)
    baker.make(Facility, 10, active=True, organisation=organisation)
    baker.make(Facility, 5, active=False, organisation=organisation)

    assert Facility.objects.count() == 15
    assert Facility.objects.active().count() == 10
    assert Facility.objects.non_active().count() == 5


class AuditAbstractBaseModelTest(TestCase):
    """Test for AuditAbstract."""

    def setUp(self):
        """Onset of testcase."""
        self.program = baker.make(Program)
        self.leo = timezone.now()
        self.jana = timezone.now() - datetime.timedelta(days=1)
        self.juzi = timezone.now() - datetime.timedelta(days=2)
        self.user_1 = baker.make(
            settings.AUTH_USER_MODEL, email=fake.email(), program=self.program
        )
        self.user_2 = baker.make(
            settings.AUTH_USER_MODEL, email=fake.email(), program=self.program
        )

    def test_validate_updated_date_greater_than_created(self):
        """Test that updated date is greater than created."""
        fake = Facility(created=self.leo, updated=self.jana)
        error_msg = "The updated date cannot be less than the created date"

        with pytest.raises(ValidationError) as ve:
            fake.validate_updated_date_greater_than_created()
        assert error_msg in ve.value.messages

    def test_preserve_created_and_created_by(self):
        """Test for preserve and created by."""
        # Create  a new instance
        fake = baker.make(
            Facility,
            created=self.jana,
            updated=self.leo,
            created_by=self.user_1.pk,
            updated_by=self.user_1.pk,
        )
        # Switch the create
        fake.created = self.juzi
        fake.save()

        assert self.jana == fake.created

        # Switch created_by
        fake.created_by = self.user_2.pk
        fake.updated_by = self.user_2.pk
        fake.save()

        assert self.user_1.pk == fake.created_by
        assert self.user_2.pk == fake.updated_by

    def test_preserve_created_and_created_by_org(self):
        """Test for preserve crated and created by org."""
        # Create  a new instance
        fake = baker.make(
            Organisation,
            created=self.jana,
            updated=self.leo,
            created_by=self.user_1.pk,
            updated_by=self.user_1.pk,
        )
        # Switch the create
        fake.created = self.juzi
        fake.save()

        assert self.jana == fake.created

        # Switch created_by
        fake.created_by = self.user_2.pk
        fake.updated_by = self.user_2.pk
        fake.save()

        assert self.user_1.pk == fake.created_by
        assert self.user_2.pk == fake.updated_by

    def test_timezone(self):
        """Test for timezone."""
        naive_datetime = timezone.now() + datetime.timedelta(500)
        with pytest.raises(ValidationError) as e:
            baker.make(Facility, created=naive_datetime)

        expected = "The updated date cannot be less than the created date"
        assert expected in e.value.messages

        instance = baker.make(Facility)
        naive_after_object_is_saved = datetime.datetime.now()
        instance.updated = naive_after_object_is_saved
        instance.save()
        instance.refresh_from_db()
        assert timezone.is_aware(instance.updated)

        # Test that we don't need to make created timezone aware
        # It is already timezone aware
        assert timezone.is_aware(instance.created)
        created_naive_datetime = datetime.datetime.now()
        instance.created = created_naive_datetime  # This should not even update
        instance.save()
        assert timezone.is_aware(instance.created)

    def test_owner(self):
        """Test for test owner."""
        org = baker.make(Organisation, name="Savannah Informatics")
        fake = baker.make(
            Facility,
            created=self.jana,
            updated=self.leo,
            created_by=self.user_1.pk,
            updated_by=self.user_1.pk,
            organisation=org,
        )
        fake.save()

        assert fake.organisation.org_code == fake.owner


class UserFacilityAllotmentTest(TestCase):
    """Tests for the UserFacilityAllotment model."""

    def setUp(self) -> None:
        self.by_both = UserFacilityAllotment.AllotmentType.BY_FACILITY_AND_REGION
        self.by_facility = UserFacilityAllotment.AllotmentType.BY_FACILITY
        self.by_region = UserFacilityAllotment.AllotmentType.BY_REGION
        self.organisation = baker.make(Organisation)
        self.program = baker.make(Program)
        self.facilities = baker.make(
            Facility,
            5,
            county="Kajiado",
            organisation=self.organisation,
        )
        self.user = baker.make(
            get_user_model(),
            name=fake.name(),
            organisation=self.organisation,
            program=self.program,
        )
        self.user_facility_allotment: UserFacilityAllotment = baker.make(
            UserFacilityAllotment,
            allotment_type=UserFacilityAllotment.AllotmentType.BY_FACILITY.value,
            facilities=self.facilities,
            organisation=self.organisation,
            user=self.user,
        )

    def test_constituency_must_be_provided_if_region_type_is_constituency(
        self,
    ):
        """Test that at least 1 constituency must be provided when region type is constituency."""

        constituency = UserFacilityAllotment.RegionType.CONSTITUENCY
        with pytest.raises(ValidationError) as e1:
            baker.make(
                UserFacilityAllotment,
                user=self.user,
                allotment_type=self.by_both.value,
                region_type=constituency.value,
            )

        with pytest.raises(ValidationError) as e2:
            baker.make(
                UserFacilityAllotment,
                user=self.user,
                allotment_type=self.by_region.value,
                region_type=constituency.value,
            )

        assert (
            'At least 1 constituency must be selected if region type is "%s"' % constituency.label
            in e1.value.messages
        )
        assert (
            'At least 1 constituency must be selected if region type is "%s"' % constituency.label
            in e2.value.messages
        )

    def test_county_must_be_provided_if_region_type_is_county(self):
        """Test that at least 1 county must be provided when region type is county."""

        county = UserFacilityAllotment.RegionType.COUNTY
        with pytest.raises(ValidationError) as e1:
            baker.make(
                UserFacilityAllotment,
                user=self.user,
                allotment_type=self.by_both.value,
                region_type=county.value,
            )

        with pytest.raises(ValidationError) as e2:
            baker.make(
                UserFacilityAllotment,
                user=self.user,
                allotment_type=self.by_region.value,
                region_type=county.value,
            )

        assert (
            'At least 1 county must be selected if region type is "%s"' % county.label
            in e1.value.messages
        )
        assert (
            'At least 1 county must be selected if region type is "%s"' % county.label
            in e2.value.messages
        )

    def test_sub_county_must_be_provided_if_region_type_is_sub_county(self):
        """Test that at least 1 sub_county must be provided when region type is sub sub_county."""

        sub_county = UserFacilityAllotment.RegionType.SUB_COUNTY
        with pytest.raises(ValidationError) as e1:
            baker.make(
                UserFacilityAllotment,
                user=self.user,
                allotment_type=self.by_both.value,
                region_type=sub_county.value,
            )

        with pytest.raises(ValidationError) as e2:
            baker.make(
                UserFacilityAllotment,
                user=self.user,
                allotment_type=self.by_region.value,
                region_type=sub_county.value,
            )

        assert (
            'At least 1 sub_county must be selected if region type is "%s"' % sub_county.label
            in e1.value.messages
        )
        assert (
            'At least 1 sub_county must be selected if region type is "%s"' % sub_county.label
            in e2.value.messages
        )

    def test_ward_must_be_provided_if_region_type_is_ward(self):
        """Test that at least 1 ward must be provided when region type is ward."""

        ward = UserFacilityAllotment.RegionType.WARD
        with pytest.raises(ValidationError) as e1:
            baker.make(
                UserFacilityAllotment,
                user=self.user,
                allotment_type=self.by_both.value,
                region_type=ward.value,
            )

        with pytest.raises(ValidationError) as e2:
            baker.make(
                UserFacilityAllotment,
                user=self.user,
                allotment_type=self.by_region.value,
                region_type=ward.value,
            )

        assert (
            'At least 1 ward must be selected if region type is "%s"' % ward.label
            in e1.value.messages
        )
        assert (
            'At least 1 ward must be selected if region type is "%s"' % ward.label
            in e2.value.messages
        )

    def test_get_facilities_for_user(self):
        """Tests for the `UserFacilityAllotment.get_facilities_for_user()` method."""

        user = baker.make(
            get_user_model(),
            name=fake.name(),
            organisation=self.organisation,
            program=self.program,
        )

        assert UserFacilityAllotment.get_facilities_for_user(user).count() == 0
        assert UserFacilityAllotment.get_facilities_for_user(self.user).count() == len(
            self.facilities
        )

    def test_region_type_must_be_provided_if_allot_by_region_or_both(self):
        """Test that a region type must be provided when allotment type is by region or both."""

        with pytest.raises(ValidationError) as e1:
            baker.make(
                UserFacilityAllotment,
                user=self.user,
                allotment_type=self.by_both.value,
                region_type=None,
            )

        with pytest.raises(ValidationError) as e2:
            baker.make(
                UserFacilityAllotment,
                user=self.user,
                allotment_type=self.by_region.value,
                region_type=None,
            )

        assert (
            'A region type must be provided if allotment type is "%s"' % self.by_both.label
            in e1.value.messages
        )
        assert (
            'A region type must be provided if allotment type is "%s"' % self.by_region.label
            in e2.value.messages
        )

    def test_representation(self):
        """Test the `self.__str__()` method."""

        assert str(self.user_facility_allotment) == "User: %s; Allotment Type: %s" % (
            self.user_facility_allotment.user.name,
            self.user_facility_allotment.get_allotment_type_display(),
        )

    def test_user_facility_allotment_by_facility(self):
        """Test that a user can be allotted individual facilities."""

        facilities = baker.make(Facility, 20, organisation=self.organisation)
        user = baker.make(
            get_user_model(),
            name=fake.name(),
            organisation=self.organisation,
            program=self.program,
        )
        allotment: UserFacilityAllotment = baker.make(
            UserFacilityAllotment,
            allotment_type=UserFacilityAllotment.AllotmentType.BY_FACILITY.value,
            facilities=facilities[10:],
            organisation=self.organisation,
            region_type=UserFacilityAllotment.RegionType.SUB_COUNTY.value,
            sub_counties=["Kajiado East"],  # This should not affect the allotted facilities count
            user=user,
        )

        assert allotment
        assert allotment.allotment_type == UserFacilityAllotment.AllotmentType.BY_FACILITY.value
        assert UserFacilityAllotment.get_facilities_for_allotment(allotment).count() == 10

        allotment.region_type = None
        allotment.save()

        assert UserFacilityAllotment.get_facilities_for_allotment(allotment).count() == 10

    def test_user_facility_allotment_by_county(self):
        """Test that a user can be allotted facilities by county."""

        baker.make(Facility, 25, county="Nairobi", organisation=self.organisation)
        user = baker.make(
            get_user_model(),
            name=fake.name(),
            organisation=self.organisation,
            program=self.program,
        )
        allotment: UserFacilityAllotment = baker.make(
            UserFacilityAllotment,
            allotment_type=UserFacilityAllotment.AllotmentType.BY_REGION.value,
            counties=["Nairobi"],
            facilities=self.facilities,  # This should not affect the allotted facilities count
            organisation=self.organisation,
            region_type=UserFacilityAllotment.RegionType.COUNTY.value,
            user=user,
        )

        assert allotment
        assert allotment.allotment_type == UserFacilityAllotment.AllotmentType.BY_REGION.value
        assert UserFacilityAllotment.get_facilities_for_allotment(allotment).count() == 25

        allotment.counties = ["Nairobi", "Kajiado"]
        allotment.save()

        # After this, the allotment should have 25 facilities in Nairobi and 5 in Kajiado.
        # The 5 facilities from Kajiado are created during this fixture setup, i.e check the
        # `self.setup()` method.
        assert UserFacilityAllotment.get_facilities_for_user(allotment.user).count() == 30

    def test_user_facility_allotment_by_both_facility_and_region(self):
        """Test that a user can be allotted facilities by both region and facility."""

        baker.make(
            Facility,
            20,
            county="Kajiado",
            organisation=self.organisation,
        )
        baker.make(
            Facility,
            30,
            county="Nairobi",
            organisation=self.organisation,
        )
        user = baker.make(
            get_user_model(),
            name=fake.name(),
            organisation=self.organisation,
            program=self.program,
        )
        allotment = baker.make(
            UserFacilityAllotment,
            allotment_type=self.by_both.value,
            facilities=self.facilities,
            organisation=self.organisation,
            region_type=UserFacilityAllotment.RegionType.WARD.value,
            wards=["Magadi"],
            user=user,
        )

        assert allotment
        assert allotment.allotment_type == self.by_both.value
        assert UserFacilityAllotment.get_facilities_for_allotment(allotment).count() == 5

        allotment.wards = ["Magadi", "Ngara"]
        allotment.save()

        assert UserFacilityAllotment.get_facilities_for_allotment(allotment).count() == 5
