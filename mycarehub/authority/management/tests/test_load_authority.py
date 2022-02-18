from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from mycarehub.authority.models import AuthorityPermission, AuthorityRole


class CommandsTestCase(TestCase):
    def test_load_authority(self):
        "Test load roles and permissions"
        out = StringIO()
        assert not AuthorityPermission.objects.exists()
        assert not AuthorityRole.objects.exists()
        call_command("load_authority", stdout=out)
        assert AuthorityPermission.objects.exists()
        assert AuthorityRole.objects.exists()
