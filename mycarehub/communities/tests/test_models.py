from datetime import timedelta

import pytest
from django.utils import timezone
from model_bakery import baker

from mycarehub.communities.models import Community, PostingHour

pytestmark = pytest.mark.django_db


def test_community_str():
    comm = baker.make(Community, name="Test Community", client_types=["PMTCT"])

    assert str(comm) == "Test Community"


def test_posting_hour_str():
    comm = baker.make(Community, name="Test Community", client_types=["PMTCT"])
    start_time = timezone.now().time()
    e_time = timezone.now() + timedelta(hours=2)
    end_time = e_time.time()

    p_hour = baker.make(PostingHour, community=comm, start=start_time, end=end_time)

    assert str(p_hour) == f"{start_time} - {end_time}"
