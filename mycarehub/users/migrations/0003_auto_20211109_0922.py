# Generated by Django 3.2.9 on 2021-11-09 06:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20211108_2027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metric',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='termsofservice',
            name='valid_from',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='userpin',
            name='valid_from',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='userpin',
            name='valid_to',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
