# Generated by Django 3.2.9 on 2021-11-20 09:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20211119_0628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='next_allowed_login',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
