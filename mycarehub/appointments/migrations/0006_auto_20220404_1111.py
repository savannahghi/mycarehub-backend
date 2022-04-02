# Generated by Django 3.2.12 on 2022-04-04 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0005_auto_20220402_1226'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='appointment_id',
        ),
        migrations.AddField(
            model_name='appointment',
            name='external_id',
            field=models.CharField(blank=True, editable=False, help_text='Identifier that is shared between KenyaEMR and MyCareHub', max_length=128, null=True, unique=True),
        ),
    ]
