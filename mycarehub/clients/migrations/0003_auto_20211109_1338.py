# Generated by Django 3.2.9 on 2021-11-09 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_alter_auditlog_timestamp'),
        ('clients', '0002_auto_20211109_0922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relatedperson',
            name='addresses',
            field=models.ManyToManyField(blank=True, null=True, related_name='related_person_addresses', to='common.Address'),
        ),
        migrations.AlterField(
            model_name='relatedperson',
            name='contacts',
            field=models.ManyToManyField(blank=True, null=True, related_name='related_person_contacts', to='common.Contact'),
        ),
    ]