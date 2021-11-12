# Generated by Django 3.2.9 on 2021-11-10 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_alter_auditlog_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='auditlog',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='facility',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='facilityattachment',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userfacilityallotment',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]