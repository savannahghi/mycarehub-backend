"""
Module for all Form Tests.
"""
from datetime import date, timedelta

import pytest
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from mycarehub.users.forms import UserCreationForm, validate_date_past
from mycarehub.users.models import User

pytestmark = pytest.mark.django_db


def test_validate_date_past():
    with pytest.raises(ValidationError):
        future_date = date.today() + timedelta(days=4)
        validate_date_past(future_date)

    with pytest.raises(ValidationError):
        validate_date_past("not a date")


class TestUserCreationForm:
    """
    Test class for all tests related to the UserCreationForm
    """

    def test_username_validation_error_msg(self, user: User):
        """
        Tests UserCreation Form's unique validator functions correctly by testing:
            1) A new user with an existing username cannot be added.
            2) Only 1 error is raised by the UserCreation Form
            3) The desired error message is raised
        """

        # The user already exists,
        # hence cannot be created.
        form = UserCreationForm(
            {
                "username": user.username,
                "password1": user.password,
                "password2": user.password,
            }
        )

        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "username" in form.errors
        assert form.errors["username"][0] == _("This username has already been taken.")
