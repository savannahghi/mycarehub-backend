import json
import os
import sys
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import transaction

from mycarehub.screeningtools.models import ScreeningToolsQuestion


class Command(BaseCommand):
    help = "Loads the screening tool questions to the database"

    @transaction.atomic
    def handle(self, *args, **options):
        base_path = Path(__file__).parent.parent.parent.parent.parent.resolve()
        sys.path.append(str(base_path))
        data_dir = os.path.join(base_path, "data")
        source_file_screeningtools = os.path.join(data_dir, "screeningtools.json")

        data_screeningtools = json.load(open(file=source_file_screeningtools))
        count = len(data_screeningtools)

        for screeningtool in data_screeningtools:
            if ScreeningToolsQuestion.objects.filter(question=screeningtool["question"]).exists():
                continue
            r, created = ScreeningToolsQuestion.objects.get_or_create(
                question=screeningtool["question"],
                tool_type=screeningtool["tool_type"],
                response_choices=screeningtool["response_choices"],
                response_type=screeningtool["response_type"],
                response_category=screeningtool["response_category"],
                sequence=screeningtool["sequence"],
                meta=screeningtool["meta"],
            )
            r.save()
            print(f"screeningtool: {screeningtool}; Created: {created}; {count}")
