# Generated by Django 3.2.9 on 2022-02-08 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0021_auto_20220203_1325'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicerequest',
            name='facility',
            field=models.TextField(blank=True, null=True),
        ),
    ]
