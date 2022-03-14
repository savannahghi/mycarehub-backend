# Generated by Django 3.2.11 on 2022-03-09 06:34

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import mycarehub.common.models.base_models
import mycarehub.utils.general_utils
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clients', '0027_alter_servicerequest_request_type'),
        ('common', '0016_auto_20220215_1721'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScreeningToolsQuestion',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.UUIDField(blank=True, null=True)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_by', models.UUIDField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('question', models.TextField()),
                ('tool_type', models.CharField(choices=[('TB_ASSESSMENT', 'TB Assessment'), ('VIOLENCE_ASSESSMENT', 'Violence Assessment'), ('CONTRACEPTIVE_ASSESSMENT', 'Contraceptive Assessment'), ('ALCOHOL_SUBSTANCE_ASSESSMENT', 'Alcohol and Substance Use Assessment')], max_length=32)),
                ('response_choices', models.JSONField(blank=True, null=True)),
                ('response_type', models.CharField(choices=[('INTEGER', 'Integer'), ('TEXT', 'Text'), ('DATE', 'Date')], max_length=32)),
                ('response_category', models.CharField(choices=[('SINGLE_CHOICE', 'Single Choice'), ('MULTI_CHOICE', 'Multiple Choice'), ('OPEN_ENDED', 'Open Ended')], max_length=32)),
                ('sequence', models.IntegerField()),
                ('meta', models.JSONField(blank=True, null=True)),
                ('organisation', models.ForeignKey(default=mycarehub.utils.general_utils.default_organisation, on_delete=django.db.models.deletion.PROTECT, related_name='screeningtools_screeningtoolsquestion_related', to='common.organisation')),
            ],
            options={
                'ordering': ('-updated', '-created'),
                'abstract': False,
            },
            managers=[
                ('objects', mycarehub.common.models.base_models.AbstractBaseManager()),
            ],
        ),
        migrations.CreateModel(
            name='ScreeningToolsResponse',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.UUIDField(blank=True, null=True)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_by', models.UUIDField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('response', models.TextField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='clients.client')),
                ('organisation', models.ForeignKey(default=mycarehub.utils.general_utils.default_organisation, on_delete=django.db.models.deletion.PROTECT, related_name='screeningtools_screeningtoolsresponse_related', to='common.organisation')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='screeningtools.screeningtoolsquestion')),
            ],
            options={
                'ordering': ('-updated', '-created'),
                'abstract': False,
            },
            managers=[
                ('objects', mycarehub.common.models.base_models.AbstractBaseManager()),
            ],
        ),
    ]