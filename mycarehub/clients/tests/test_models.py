import pytest
from model_bakery import baker

from mycarehub.clients.models import (
    Client,
    Identifier,
    RelatedPerson,
    SecurityQuestion,
    SecurityQuestionResponse,
)
from mycarehub.users.models import User

pytestmark = pytest.mark.django_db


def test_identifier_str():
    identifier = baker.make(
        Identifier,
        identifier_value="222",
        identifier_type="NATIONAL_ID",
        identifier_use="OFFICIAL",
    )
    assert str(identifier) == "222 (NATIONAL_ID, OFFICIAL)"


def test_related_person_str():
    related_person = baker.make(
        RelatedPerson,
        first_name="Juha",
        last_name="Mwenyewe",
        other_name="Kalulu",
        relationship_type="SPOUSE",
    )
    assert str(related_person) == "Juha Kalulu Mwenyewe (SPOUSE)"


def test_client_str(user_with_all_permissions):
    client = baker.make(Client, user=user_with_all_permissions, client_type="PMTCT")
    assert str(client) == f"{user_with_all_permissions.name} (PMTCT)"


def test_security_question_str():
    qn = baker.make(SecurityQuestion, stem="swali")
    assert str(qn) == "swali"


def test_security_question_response_str():
    qn = baker.make(SecurityQuestion, stem="swali")
    user = baker.make(User, name="Juha Kalulu")
    resp = baker.make(SecurityQuestionResponse, question=qn, user=user)
    assert str(resp) == "Response to 'swali' by 'Juha Kalulu'"
