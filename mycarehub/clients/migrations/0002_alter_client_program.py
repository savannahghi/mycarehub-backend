# Generated by Django 3.2.16 on 2023-01-20 12:01

from django.db import migrations, models
import django.db.models.deletion
import mycarehub.utils.general_utils


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_initial'),
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='program',
            field=models.ForeignKey(default=mycarehub.utils.general_utils.default_program, on_delete=django.db.models.deletion.PROTECT, related_name='clients', to='common.program'),
        ),
    ]
