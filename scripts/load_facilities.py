#!/usr/bin/env python
import os
import sys
from pathlib import Path

import django
import pyexcel
from django.core.exceptions import ValidationError


def get_created_by_pk():
    from mycarehub.users.models import User

    return User.objects.filter(is_staff=True)[0].pk


def get_organisation():
    from mycarehub.common.models import Organisation

    return Organisation.objects.get(code=1)


def load_facilities(source_path):
    from mycarehub.common.models import Facility

    created_by = get_created_by_pk()
    org = get_organisation()

    records = pyexcel.get_records(file_name=source_path)
    count = len(records)
    for pos, r in enumerate(records):
        if r["MFL Code"] is not None and r["MFL Code"] != "None":
            try:
                facility, created = Facility.objects.get_or_create(
                    mfl_code=r["MFL Code"],
                    defaults={
                        "name": r["Facility"],
                        "created_by": created_by,
                        "updated_by": created_by,
                        "organisation": org,
                        "sub_county": r["Sub-county"],
                    },
                )
                print(f"Facility: {facility}; Created: {created}; Pos {pos + 1}/{count}")
            except ValidationError as e:
                print(f"can't save row {r}, got error {e}")


if __name__ == "__main__":
    base_path = Path(__file__).parent.parent.resolve()
    print(base_path)
    sys.path.append(str(base_path))
    sys.path.append(str(base_path / "mycarehub"))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
    django.setup()

    data_dir = os.path.join(base_path, "data")
    source_file = os.path.join(data_dir, "List_of_PHP_study facilities.xlsx")
    load_facilities(source_file)
