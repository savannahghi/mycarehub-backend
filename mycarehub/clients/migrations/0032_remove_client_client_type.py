# Generated by Django 3.2.11 on 2022-04-25 08:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0031_alter_relatedperson_gender'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='client_type',
        ),
    ]
