# Generated by Django 3.2.16 on 2023-01-10 08:43

from django.db import migrations, models
import django.db.models.deletion
import mycarehub.utils.general_utils


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0027_auto_20230110_1143'),
        ('users', '0024_auto_20230107_0014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='program',
            field=models.ForeignKey(blank=True, default=mycarehub.utils.general_utils.default_program, null=True, on_delete=django.db.models.deletion.PROTECT, to='common.program'),
        ),
    ]
