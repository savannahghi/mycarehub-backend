# Generated by Django 3.2.14 on 2022-12-12 18:12

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers
import wagtail.models.collections
import wagtail.search.index


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0004_alter_taggeditem_content_type_alter_taggeditem_tag'),
        ('common', '0025_auto_20220909_1417'),
        ('wagtailcore', '0078_referenceindex'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('content', '0004_auto_20221212_1835'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('file', models.FileField(upload_to='media', verbose_name='file')),
                ('type', models.CharField(choices=[('audio', 'Audio file'), ('video', 'Video file')], max_length=255)),
                ('duration', models.FloatField(blank=True, default=0, help_text='Duration in seconds', validators=[django.core.validators.MinValueValidator(0)], verbose_name='duration')),
                ('width', models.PositiveIntegerField(blank=True, null=True, verbose_name='width')),
                ('height', models.PositiveIntegerField(blank=True, null=True, verbose_name='height')),
                ('thumbnail', models.FileField(blank=True, upload_to='media_thumbnails', verbose_name='thumbnail')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('collection', models.ForeignKey(default=wagtail.models.collections.get_root_collection_id, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailcore.collection', verbose_name='collection')),
                ('organisation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='content_custommedia_related', to='common.organisation')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text=None, through='taggit.TaggedItem', to='taggit.Tag', verbose_name='tags')),
                ('uploaded_by_user', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='uploaded by user')),
            ],
            options={
                'verbose_name': 'media',
                'abstract': False,
            },
            bases=(wagtail.search.index.Indexed, models.Model),
        ),
    ]