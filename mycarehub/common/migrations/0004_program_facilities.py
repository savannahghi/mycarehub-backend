# Generated by Django 3.2.16 on 2023-01-25 12:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("common", "0003_auto_20230124_1200"),
    ]

    operations = [
        migrations.AddField(
            model_name="program",
            name="facilities",
            field=models.ManyToManyField(
                blank=True, null=True, related_name="programs", to="common.Facility"
            ),
        ),
    ]
