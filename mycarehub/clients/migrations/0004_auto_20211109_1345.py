# Generated by Django 3.2.9 on 2021-11-09 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_alter_auditlog_timestamp'),
        ('clients', '0003_auto_20211109_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='addresses',
            field=models.ManyToManyField(blank=True, null=True, related_name='client_addresses', to='common.Address'),
        ),
        migrations.AlterField(
            model_name='client',
            name='contacts',
            field=models.ManyToManyField(blank=True, null=True, related_name='client_contacts', to='common.Contact'),
        ),
        migrations.AlterField(
            model_name='client',
            name='related_persons',
            field=models.ManyToManyField(blank=True, null=True, related_name='client_related_persons', to='clients.RelatedPerson'),
        ),
        migrations.AlterField(
            model_name='client',
            name='treatment_buddy',
            field=models.TextField(blank=True, null=True),
        ),
    ]
