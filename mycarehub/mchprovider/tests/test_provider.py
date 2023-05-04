import json
import warnings
from unittest.mock import MagicMock

import pytest
from allauth.account.models import EmailAddress
from allauth.account.utils import get_user_model, user_email, user_username
from allauth.socialaccount import app_settings
from allauth.socialaccount.providers.base import ProviderException
from allauth.socialaccount.tests import OAuth2TestsMixin
from allauth.tests import MockedResponse, TestCase
from django.test.utils import override_settings
from django.urls import reverse
from faker import Faker
from model_bakery import baker

from mycarehub.common.models import Facility, Organisation, Program
from mycarehub.mchprovider.provider import MycarehubProvider

fake = Faker()

pytestmark = pytest.mark.django_db

help_text = "Please contact the help center for assistance."


class MCHProviderTests(OAuth2TestsMixin, TestCase):
    provider_id = MycarehubProvider.id

    def get_mocked_response(self):
        data = {
            "username": fake.user_name(),
            "sub": fake.name(),
            "gender": "male",
            "user_id": fake.uuid4(),
            "staff_id": fake.uuid4(),
            "program_id": fake.uuid4(),
            "facility_id": fake.uuid4(),
            "is_superuser": False,
            "organisation_id": fake.uuid4(),
            "is_program_admin": False,
            "is_organisation_admin": False,
        }

        return MockedResponse(
            200,
            json.dumps(data),
        )

    @override_settings(SOCIALACCOUNT_AUTO_SIGNUP=False)
    def test_login(self):
        resp_mock = self.get_mocked_response()
        if not resp_mock:
            warnings.warn("Cannot test provider %s, no oauth mock" % self.provider.id)
            return
        resp = self.login(
            resp_mock,
        )
        self.assertRedirects(resp, reverse("wagtailadmin_login"))

    @override_settings(SOCIALACCOUNT_AUTO_SIGNUP=False)
    def test_login_with_pkce_disabled(self):
        provider_settings = app_settings.PROVIDERS.get(self.provider_id, {})
        provider_settings_with_pkce_disabled = provider_settings.copy()
        provider_settings_with_pkce_disabled["OAUTH_PKCE_ENABLED"] = False

        with self.settings(
            SOCIALACCOUNT_PROVIDERS={self.provider_id: provider_settings_with_pkce_disabled}
        ):
            resp_mock = self.get_mocked_response()
            if not resp_mock:
                warnings.warn("Cannot test provider %s, no oauth mock" % self.provider.id)
                return
            resp = self.login(
                resp_mock,
            )
            self.assertRedirects(resp, reverse("wagtailadmin_login"))

    @override_settings(SOCIALACCOUNT_AUTO_SIGNUP=False)
    def test_login_with_pkce_enabled(self):
        provider_settings = app_settings.PROVIDERS.get(self.provider_id, {})
        provider_settings_with_pkce_enabled = provider_settings.copy()
        provider_settings_with_pkce_enabled["OAUTH_PKCE_ENABLED"] = True
        with self.settings(
            SOCIALACCOUNT_PROVIDERS={self.provider_id: provider_settings_with_pkce_enabled}
        ):
            resp_mock = self.get_mocked_response()
            if not resp_mock:
                warnings.warn("Cannot test provider %s, no oauth mock" % self.provider.id)
                return

            resp = self.login(
                resp_mock,
            )
            self.assertRedirects(resp, reverse("wagtailadmin_login"))

    def test_authentication_error(self):
        resp = self.client.get(reverse(self.provider.id + "_callback"))
        assert resp is not None

    def test_account_tokens(self, multiple_login=False):
        if not app_settings.STORE_TOKENS:
            return
        email = "user@example.com"
        user = get_user_model()(is_active=True)
        user_email(user, email)
        user_username(user, "user")
        user.set_password("test")
        user.save()
        EmailAddress.objects.create(user=user, email=email, primary=True, verified=True)
        self.client.login(username=user.username, password="test")
        self.login(self.get_mocked_response(), process="connect")
        if multiple_login:
            self.login(
                self.get_mocked_response(),
                with_refresh_token=False,
                process="connect",
            )


class TestAdapters:
    def test_get_default_scope(self):
        req = MagicMock()
        provider = MycarehubProvider(req)

        assert provider.get_default_scope() == []

    def test_extract_uid(self):
        req = MagicMock()
        provider = MycarehubProvider(req)

        id = fake.uuid4()
        data = {"staff_id": id}

        assert provider.extract_uid(data) == id

    def test_extract_common_fields_invalid_organisation_id(self):
        req = MagicMock()
        provider = MycarehubProvider(req)

        org_id = fake.uuid4()
        data = {"organisation_id": org_id, "staff_id": fake.uuid4()}

        with pytest.raises(ProviderException) as e:
            provider.extract_common_fields(data)
            assert str(e) == f"Selected Organisation does not exist on the CMS.{help_text}"

    def test_extract_common_fields_invalid_program_id(self):
        req = MagicMock()
        provider = MycarehubProvider(req)

        org_id = fake.uuid4()
        data = {"organisation_id": org_id, "program_id": fake.uuid4(), "staff_id": fake.uuid4()}
        baker.make(Organisation, id=org_id)

        with pytest.raises(ProviderException) as e:
            provider.extract_common_fields(data)
            assert str(e) == f"Selected Program does not exist on the CMS.{help_text}"

    def test_extract_common_fields_invalid_facility_id(self):
        req = MagicMock()
        provider = MycarehubProvider(req)

        org_id = fake.uuid4()
        program_id = fake.uuid4()
        facility_id = fake.uuid4()
        data = {
            "organisation_id": org_id,
            "program_id": program_id,
            "facility_id": facility_id,
            "staff_id": fake.uuid4(),
        }

        baker.make(Organisation, id=org_id)
        baker.make(Program, id=program_id)

        with pytest.raises(ProviderException) as e:
            provider.extract_common_fields(data)
            assert str(e) == f"Selected Facility does not exist on the CMS.{help_text}"

    def test_extract_common_fields(self):
        req = MagicMock()
        provider = MycarehubProvider(req)

        org_id = fake.uuid4()
        program_id = fake.uuid4()
        facility_id = fake.uuid4()
        data = {
            "organisation_id": org_id,
            "program_id": program_id,
            "facility_id": facility_id,
            "staff_id": fake.uuid4(),
            "sub": fake.name(),
            "gender": "male",
            "username": fake.user_name(),
        }

        baker.make(Organisation, id=org_id)
        baker.make(Program, id=program_id)
        baker.make(Facility, id=facility_id)

        provider.extract_common_fields(data)
