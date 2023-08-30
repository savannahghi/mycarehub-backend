# Generated by Django 3.2.16 on 2023-01-20 07:32

import uuid

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models

import mycarehub.common.models.base_models
import mycarehub.utils.general_utils


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("common", "0002_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Client",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False
                    ),
                ),
                ("active", models.BooleanField(default=True)),
                ("created", models.DateTimeField(default=django.utils.timezone.now)),
                ("created_by", models.UUIDField(blank=True, null=True)),
                ("updated", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_by", models.UUIDField(blank=True, null=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "name",
                    models.CharField(blank=True, max_length=255, verbose_name="Name of Client"),
                ),
                (
                    "gender",
                    models.CharField(
                        blank=True,
                        choices=[("MALE", "Male"), ("FEMALE", "Female"), ("OTHER", "Other")],
                        max_length=16,
                        null=True,
                    ),
                ),
                ("date_of_birth", models.DateField(blank=True, null=True)),
                (
                    "organisation",
                    models.ForeignKey(
                        default=mycarehub.utils.general_utils.default_organisation,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="clients_client_related",
                        to="common.organisation",
                    ),
                ),
                (
                    "program",
                    models.ForeignKey(
                        default=mycarehub.utils.general_utils.default_program,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="common.program",
                    ),
                ),
            ],
            options={
                "ordering": ("-updated", "-created"),
                "abstract": False,
            },
            managers=[
                ("objects", mycarehub.common.models.base_models.AbstractBaseManager()),
            ],
        ),
    ]
