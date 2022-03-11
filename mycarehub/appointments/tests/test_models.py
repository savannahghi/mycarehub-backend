import pytest
from model_bakery import baker

from mycarehub.appointments.models import Appointment
from mycarehub.clients.models import Client

pytestmark = pytest.mark.django_db


def test_appointments_str(user):
    client = baker.make(Client, user=user)
    appointment = baker.make(
        Appointment,
        appointment_type="consultation",
        status="COMPLETED",
        client=client,
    )

    assert str(appointment) == f"{client} - consultation - COMPLETED"
