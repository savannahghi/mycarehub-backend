# Generated by Django 3.2.16 on 2023-01-18 13:13

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import mycarehub.common.models.base_models
import taggit.managers
import uuid
import wagtail.fields
import wagtail.models.collections
import wagtail.search.index


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0004_alter_taggeditem_content_type_alter_taggeditem_tag'),
        ('wagtailcore', '0078_referenceindex'),
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.UUIDField(blank=True, null=True)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_by', models.UUIDField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(help_text="Author's name (will be displayed publicly)", max_length=128)),
            ],
            options={
                'verbose_name_plural': 'authors',
                'ordering': ('-updated', '-created'),
                'abstract': False,
            },
            managers=[
                ('objects', mycarehub.common.models.base_models.AbstractBaseManager()),
            ],
        ),
        migrations.CreateModel(
            name='ContentBookmark',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.UUIDField(blank=True, null=True)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_by', models.UUIDField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
            ],
            managers=[
                ('objects', mycarehub.common.models.base_models.AbstractBaseManager()),
            ],
        ),
        migrations.CreateModel(
            name='ContentItem',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('date', models.DateField(help_text='This will be shown to readers as the publication date', verbose_name='Post date')),
                ('intro', models.CharField(help_text="A teaser that will be shown when it's inappropriate to show the entire article", max_length=250)),
                ('item_type', models.CharField(choices=[('ARTICLE', 'Article'), ('AUDIO_VIDEO', 'Audio Video'), ('PDF_DOCUMENT', 'Pdf Document')], help_text='Whether this item is an article, audio/video or document. This is used by the mobile app to determine how to render content. e.g with an article, the layout will be hero_image > body while for audio-visual content the media will come first and the body last. For documents, the document(s) will also be presented before the body text.', max_length=64)),
                ('time_estimate_seconds', models.PositiveIntegerField(default=0, help_text='An estimate of how long it will take to read the article, in seconds. The mobile app(s) and website will render this in a more friendly form e.g minutes, hours etc.')),
                ('body', wagtail.fields.RichTextField(help_text='The main article text, video description, audio file description or document description.')),
                ('like_count', models.PositiveIntegerField(default=0)),
                ('bookmark_count', models.PositiveIntegerField(default=0)),
                ('share_count', models.PositiveIntegerField(default=0)),
                ('view_count', models.PositiveIntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='ContentItemCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='A standard name for a type of content e.g fitness, diet etc. These will be used in the user interface to group content so they should be chosen carefully.', max_length=255)),
            ],
            options={
                'verbose_name_plural': 'content item categories',
            },
            bases=(wagtail.search.index.Indexed, models.Model),
        ),
        migrations.CreateModel(
            name='ContentItemDocumentLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContentItemGalleryImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('caption', models.CharField(blank=True, max_length=250)),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ContentItemIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('intro', wagtail.fields.RichTextField(default='myCareHub', help_text="The content site's tagline")),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='ContentItemMediaLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContentItemQuestionnaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContentItemTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ContentItemTagIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='ContentLike',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.UUIDField(blank=True, null=True)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_by', models.UUIDField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
            ],
            managers=[
                ('objects', mycarehub.common.models.base_models.AbstractBaseManager()),
            ],
        ),
        migrations.CreateModel(
            name='ContentShare',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.UUIDField(blank=True, null=True)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_by', models.UUIDField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
            ],
            managers=[
                ('objects', mycarehub.common.models.base_models.AbstractBaseManager()),
            ],
        ),
        migrations.CreateModel(
            name='ContentView',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.UUIDField(blank=True, null=True)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_by', models.UUIDField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
            ],
            managers=[
                ('objects', mycarehub.common.models.base_models.AbstractBaseManager()),
            ],
        ),
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
            ],
            options={
                'verbose_name': 'media',
                'abstract': False,
            },
            bases=(wagtail.search.index.Indexed, models.Model),
        ),
    ]
