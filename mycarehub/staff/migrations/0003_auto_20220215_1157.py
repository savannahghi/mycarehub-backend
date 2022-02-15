# Generated by Django 3.2.9 on 2022-02-15 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0026_servicerequest_facility'),
        ('common', '0015_faq'),
        ('staff', '0002_alter_staff_default_facility'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='addresses',
            field=models.ManyToManyField(blank=True, related_name='staff_addresses', to='common.Address'),
        ),
        migrations.AddField(
            model_name='staff',
            name='contacts',
            field=models.ManyToManyField(blank=True, related_name='staff_contacts', to='common.Contact'),
        ),
        migrations.AddField(
            model_name='staff',
            name='identifiers',
            field=models.ManyToManyField(related_name='staff_identifiers', to='clients.Identifier'),
        ),
    ]
