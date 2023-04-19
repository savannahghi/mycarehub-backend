import requests
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)
from django.conf import settings
from requests.auth import HTTPBasicAuth

from .provider import MycarehubProvider

ACCESS_TOKEN_URL = (
    getattr(settings, "SOCIALACCOUNT_PROVIDERS", {})
    .get("mycarehub", {})
    .get("ACCESS_TOKEN_URL", "")
)

AUTHORIZE_URL = (
    getattr(settings, "SOCIALACCOUNT_PROVIDERS", {}).get("mycarehub", {}).get("AUTHORIZE_URL", "")
)

INTROSPECT_URL = (
    getattr(settings, "SOCIALACCOUNT_PROVIDERS", {}).get("mycarehub", {}).get("INTROSPECT_URL", "")
)


class MCHOAuth2Adapter(OAuth2Adapter):
    provider_id = MycarehubProvider.id
    supports_state = True

    access_token_url = ACCESS_TOKEN_URL
    authorize_url = AUTHORIZE_URL
    introspect_url = INTROSPECT_URL

    def complete_login(self, request, app, token, response):
        payload = f"token={token}"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        resp = requests.post(
            self.introspect_url,
            headers=headers,
            data=payload,
            auth=HTTPBasicAuth(app.client_id, app.secret),
        )
        resp.raise_for_status()
        extra_data = resp.json()

        return self.get_provider().sociallogin_from_response(request, extra_data)


oauth2_login = OAuth2LoginView.adapter_view(MCHOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(MCHOAuth2Adapter)
