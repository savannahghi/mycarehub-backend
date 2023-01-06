# Generated by Django 3.2.16 on 2023-01-06 21:14

from django.db import migrations, models
import django.db.models.deletion
import mycarehub.utils.general_utils


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0026_program'),
        ('users', '0023_auto_20220906_1131'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': [('can_view_dashboard', 'Can View Dashboard'), ('can_view_about', 'Can View About Page'), ('can_export_data', 'Can Export Data'), ('can_import_data', 'Can Import Data'), ('system_administration', 'System Administration'), ('content_management', 'Content Management'), ('client_management', 'Client Management')], 'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.RemoveField(
            model_name='user',
            name='approval_notified',
        ),
        migrations.RemoveField(
            model_name='user',
            name='avatar',
        ),
        migrations.RemoveField(
            model_name='user',
            name='failed_login_count',
        ),
        migrations.RemoveField(
            model_name='user',
            name='failed_security_count',
        ),
        migrations.RemoveField(
            model_name='user',
            name='flavour',
        ),
        migrations.RemoveField(
            model_name='user',
            name='handle',
        ),
        migrations.RemoveField(
            model_name='user',
            name='has_set_nickname',
        ),
        migrations.RemoveField(
            model_name='user',
            name='has_set_pin',
        ),
        migrations.RemoveField(
            model_name='user',
            name='has_set_security_questions',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_approved',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_phone_verified',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_suspended',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_failed_login',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_successful_login',
        ),
        migrations.RemoveField(
            model_name='user',
            name='next_allowed_login',
        ),
        migrations.RemoveField(
            model_name='user',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='user',
            name='pin_change_required',
        ),
        migrations.RemoveField(
            model_name='user',
            name='pin_update_required',
        ),
        migrations.RemoveField(
            model_name='user',
            name='push_tokens',
        ),
        migrations.RemoveField(
            model_name='user',
            name='terms_accepted',
        ),
        migrations.AddField(
            model_name='user',
            name='program',
            field=models.ForeignKey(blank=True, default=mycarehub.utils.general_utils.default_organisation, null=True, on_delete=django.db.models.deletion.PROTECT, to='common.program'),
        ),
    ]