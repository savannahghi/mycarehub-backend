from unittest.mock import MagicMock

import pytest
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.providers.base import ProviderException
from faker import Faker

from mycarehub.users.adapters import AccountAdapter, SocialAccountAdapter

fake = Faker()


class TestAdapters:
    def test_is_open_for_signup(self):
        req = MagicMock()
        social_login = MagicMock()

        account_adapter = AccountAdapter()
        assert account_adapter.is_open_for_signup(request=req) is True

        social_adapter = SocialAccountAdapter()
        assert social_adapter.is_open_for_signup(request=req, sociallogin=social_login) is True

    def test_populate_user(self):
        req = MagicMock()
        social_login = MagicMock()
        social_adapter = SocialAccountAdapter()

        assert (
            social_adapter.populate_user(request=req, sociallogin=social_login, data={})
            is not None
        )

        data = {"program_id": fake.uuid4()}

        assert (
            social_adapter.populate_user(request=req, sociallogin=social_login, data=data)
            is not None
        )

        data["organisation_id"] = fake.uuid4()
        assert (
            social_adapter.populate_user(request=req, sociallogin=social_login, data=data)
            is not None
        )

        data["is_program_admin"] = True
        assert (
            social_adapter.populate_user(request=req, sociallogin=social_login, data=data)
            is not None
        )

        data["is_organisation_admin"] = True
        assert (
            social_adapter.populate_user(request=req, sociallogin=social_login, data=data)
            is not None
        )

    def test_authentication_error(self):
        req = MagicMock()
        social_adapter = SocialAccountAdapter()

        with pytest.raises(ImmediateHttpResponse):
            social_adapter.authentication_error(
                request=req, provider_id="id", exception=ProviderException("not good")
            )

        with pytest.raises(ImmediateHttpResponse):
            social_adapter.authentication_error(request=req, provider_id="id")
