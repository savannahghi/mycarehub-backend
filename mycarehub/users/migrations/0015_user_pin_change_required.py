# Generated by Django 3.2.9 on 2021-11-21 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_alter_user_next_allowed_login'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='pin_change_required',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]
