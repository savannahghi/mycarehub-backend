from django.conf import settings
from social_core.backends.oauth import BaseOAuth2

class MycarehubOAuth2(BaseOAuth2):
    """Mycarehub OAuth2."""

    def __init__(self) -> None:
            """Mycarehub OAuth2 constructor."""
            self.client_id = settings.MCH_OAUTH2_CLIENT_ID
            self.client_sectet = settings.MCH_OAUTH2_CLIENT_SECRET
            self.introspect_url = settings.MCH_OAUTH2_INTROSPECT_URL
            self.name = "mycarehub-oauth2"


    def user_data(self, access_token, *args, **kwargs):
        """Get user data from mycarehub."""
        headers = {"Authorization": "Bearer {}".format(access_token)}

        response = self.get_json(settings.MCH_USER_PROFILE_URL, method="GET", headers=headers)
        return response
