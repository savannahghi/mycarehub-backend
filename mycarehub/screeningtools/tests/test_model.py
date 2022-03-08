import pytest
from model_bakery import baker

from mycarehub.clients.models import Client
from mycarehub.screeningtools.models import ScreeningToolsQuestion, ScreeningToolsResponse

pytestmark = pytest.mark.django_db


def test_screeningtools_question():
    question = baker.make(
        ScreeningToolsQuestion,
        question="question",
        tool_type="TB_ASSESSMENT",
        response_choices="{'0': 'Yes', '1': 'No'}",
        response_type="INTEGER",
        response_category="SINGLE_CHOICE",
    )
    assert str(question) == "question"


def test_screeningtools_response(user_with_all_permissions):
    response = baker.make(
        ScreeningToolsResponse,
        question=baker.make(
            ScreeningToolsQuestion,
            question="question",
            tool_type="TB_ASSESSMENT",
            response_choices="{'0': 'Yes', '1': 'No'}",
            response_type="INTEGER",
            response_category="SINGLE_CHOICE",
        ),
        client=baker.make(Client, user=user_with_all_permissions, client_type="PMTCT"),
        response="0",
    )
    assert str(response) == "0"
