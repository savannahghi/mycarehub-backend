# Generated by Django 3.2.9 on 2021-11-16 12:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_userpin_salt'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserOTP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_valid', models.BooleanField()),
                ('generated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('valid_until', models.DateTimeField(blank=True, null=True)),
                ('channel', models.CharField(max_length=10)),
                ('flavour', models.CharField(choices=[('PRO', 'PRO'), ('CONSUMER', 'CONSUMER')], max_length=32, null=True)),
                ('phonenumber', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
