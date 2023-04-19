import pytest
from django.urls import reverse
from rest_framework import status

from mycarehub.common.views import HomeView

pytestmark = pytest.mark.django_db


def test_approved_mixin_approved_user(rf, user_with_all_permissions):
    approved_user = user_with_all_permissions
    url = "/"
    request = rf.get(url)
    request.user = approved_user
    view = HomeView()
    view.setup(request)
    view.dispatch(request)  # no error raised


def test_home_view(user_with_all_permissions, client):
    client.force_login(user_with_all_permissions)
    url = reverse("home")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_about_view(user_with_all_permissions, client):
    client.force_login(user_with_all_permissions)
    url = reverse("about")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_facility_view(user_with_all_permissions, client):
    client.force_login(user_with_all_permissions)
    url = reverse("common:facilities")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_user_facility_allotment_view(user_with_all_permissions, client):
    client.force_login(user_with_all_permissions)
    url = reverse("common:user_facility_allotments")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
