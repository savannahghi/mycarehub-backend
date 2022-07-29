import pytest
from model_bakery import baker

from mycarehub.questionnaires.models import (
    Question,
    QuestionInputChoice,
    Questionnaire,
    QuestionnaireResponse,
    ResponseInstance,
    ScreeningTool,
)

pytestmark = pytest.mark.django_db


def test_questionnaire_model():
    questionnaire = baker.make(Questionnaire)
    assert questionnaire.__str__() == questionnaire.name


def test_screening_tool_model():
    screening_tool = baker.make(ScreeningTool)
    assert screening_tool.__str__() == screening_tool.questionnaire.name


def test_question_model():
    question = baker.make(Question)
    assert question.__str__() == question.text


def test_question_input_choice_model():
    question_input_choice = baker.make(QuestionInputChoice)
    assert (
        question_input_choice.__str__()
        == question_input_choice.choice + ":" + question_input_choice.value
    )


def test_question_response_model():
    question_response = baker.make(QuestionnaireResponse)
    assert (
        question_response.__str__()
        == question_response.questionnaire.name
        + " response for "
        + question_response.user.username
    )


def test_response_instance_model():
    response_instance = baker.make(ResponseInstance)
    assert response_instance.__str__() == response_instance.answer
