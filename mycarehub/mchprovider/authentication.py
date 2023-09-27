import requests
from django.conf import settings
from requests.auth import HTTPBasicAuth
from rest_framework import authentication

from mycarehub.mchprovider.oauth2 import MycarehubOAuth2


class MycarehubOAuth2TokenBackend(MycarehubOAuth2):
    """Mycarehub OAuth2 token authentication backend."""

    name = "mycarehub-oauth2-token-backend"


class MycarehubOAuth2Token(authentication.BaseAuthentication):
    """Mycarehub OAuth2 backend authentication class."""

    def __init__(self) -> None:
        """Mycarehub authentication backend constructor."""
        self.client_id = settings.MCH_OAUTH2_CLIENT_ID
        self.client_sectet = settings.MCH_OAUTH2_CLIENT_SECRET
        self.introspect_url = settings.MCH_OAUTH2_INTROSPECT_URL


    def authenticate(self, request, token=None):
        """"""
        payload = f"token={token}"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = requests.post(
            self.introspect_url,
            headers=headers,
            data=payload,
            auth=HTTPBasicAuth(self.client_id, self.client_sectet),
        )

        data = response.json()
        return data, payload
