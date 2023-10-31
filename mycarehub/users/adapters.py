from typing import Any

from allauth.account.adapter import DefaultAccountAdapter
from allauth.core.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest, sociallogin: Any):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)

        if "organisation_id" in data:
            user.organisation_id = data["organisation_id"]

        if "program_id" in data:
            user.program_id = data["program_id"]

        if "is_program_admin" in data:
            pass
        if "is_organisation_admin" in data:
            pass

        user.is_superuser = data.get("is_superuser", False)

        return user

    def authentication_error(
        self,
        request,
        provider_id,
        error=None,
        exception=None,
        extra_context=None,
    ):
        if exception is not None:
            messages.add_message(request, messages.ERROR, str(exception))

        raise ImmediateHttpResponse(redirect(reverse("wagtailadmin_login")))

    def get_connect_redirect_url(self, request, socialaccount):
        """
        Returns the default URL to redirect to after successfully
        connecting a social account.
        """
        url = reverse("wagtailadmin_redirect")
        return url
