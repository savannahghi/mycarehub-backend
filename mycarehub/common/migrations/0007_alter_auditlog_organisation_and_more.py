# Generated by Django 4.1.9 on 2023-05-04 13:46

import django.db.models.deletion
from django.db import migrations, models

import mycarehub.utils.general_utils


class Migration(migrations.Migration):
    dependencies = [
        ("common", "0006_auto_20230214_1434"),
    ]

    operations = [
        migrations.AlterField(
            model_name="auditlog",
            name="organisation",
            field=models.ForeignKey(
                default=mycarehub.utils.general_utils.default_organisation,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="%(app_label)s_%(class)s_related",
                to="common.organisation",
            ),
        ),
        migrations.AlterField(
            model_name="facility",
            name="organisation",
            field=models.ForeignKey(
                default=mycarehub.utils.general_utils.default_organisation,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="%(app_label)s_%(class)s_related",
                to="common.organisation",
            ),
        ),
        migrations.AlterField(
            model_name="program",
            name="organisation",
            field=models.ForeignKey(
                default=mycarehub.utils.general_utils.default_organisation,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="%(app_label)s_%(class)s_related",
                to="common.organisation",
            ),
        ),
        migrations.AlterField(
            model_name="userfacilityallotment",
            name="organisation",
            field=models.ForeignKey(
                default=mycarehub.utils.general_utils.default_organisation,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="%(app_label)s_%(class)s_related",
                to="common.organisation",
            ),
        ),
    ]
