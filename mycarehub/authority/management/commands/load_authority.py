import json
import os
import sys
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import transaction

from mycarehub.authority.models import AuthorityPermission, AuthorityRole


class Command(BaseCommand):
    help = "Loads the roles and permissions to the database"

    @transaction.atomic
    def handle(self, *args, **options):
        base_path = Path(__file__).parent.parent.parent.parent.parent.resolve()
        sys.path.append(str(base_path))
        data_dir = os.path.join(base_path, "data")
        source_file_authority = os.path.join(data_dir, "authority.json")

        data_authority = json.load(open(file=source_file_authority))
        count = len(data_authority)

        for role_permission in data_authority:
            role = role_permission["role"]
            r, created = AuthorityRole.objects.get_or_create(
                name=role,
            )
            for permission in role_permission["permissions"]:
                p, _ = AuthorityPermission.objects.get_or_create(
                    name=permission,
                )
                r.permissions.add(p)
            print(f"role_permission: {role_permission}; Created: {created}; {count}")
