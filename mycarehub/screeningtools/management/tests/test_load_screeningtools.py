from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from mycarehub.screeningtools.models import ScreeningToolsQuestion


class CommandsTestCase(TestCase):
    def test_load_screeningquestions(self):
        "Test load screening tools"
        out = StringIO()
        assert not ScreeningToolsQuestion.objects.exists()
        call_command("load_screeningquestions", stdout=out)
        assert ScreeningToolsQuestion.objects.exists()
        lenObjects = ScreeningToolsQuestion.objects.count()
        call_command("load_screeningquestions", stdout=out)
        assert ScreeningToolsQuestion.objects.count() == lenObjects
