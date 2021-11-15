# Generated by Django 3.2.9 on 2021-11-19 03:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import modelcluster.contrib.taggit
import modelcluster.fields
import mycarehub.common.models.base_models
import mycarehub.content.models
import mycarehub.users.models
import uuid
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('common', '0010_auto_20211119_0628'),
        ('wagtailmedia', '0004_duration_optional_floatfield'),
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('wagtailcore', '0066_collection_management_permissions'),
        ('wagtailredirects', '0006_redirect_increase_max_length'),
        ('wagtailimages', '0023_add_choose_permissions'),
        ('wagtailsearchpromotions', '0002_capitalizeverbose'),
        ('wagtailforms', '0004_add_verbose_name_plural'),
        ('wagtaildocs', '0012_uploadeddocument'),
        ('content', '0001_initial'),
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
                ('avatar', models.ForeignKey(blank=True, help_text='An optional author picture (will be displayed publicly)', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='author_image', to='wagtailimages.image')),
                ('organisation', models.ForeignKey(default=mycarehub.users.models.default_organisation, on_delete=django.db.models.deletion.PROTECT, related_name='content_author_related', to='common.organisation')),
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
                ('body', wagtail.core.fields.RichTextField(help_text='The main article text, video description, audio file description or document description.')),
                ('like_count', models.PositiveIntegerField(default=0)),
                ('bookmark_count', models.PositiveIntegerField(default=0)),
                ('share_count', models.PositiveIntegerField(default=0)),
                ('view_count', models.PositiveIntegerField(default=0)),
                ('author', models.ForeignKey(help_text="The item's author. This will be displayed on the website and apps.", on_delete=django.db.models.deletion.PROTECT, to='content.author')),
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
                ('icon', models.ForeignKey(blank=True, help_text='An optional icon for the content item category. This will be shown in the user interface so it should be chosen with care.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'verbose_name_plural': 'content item categories',
            },
        ),
        migrations.CreateModel(
            name='ContentItemDocumentLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('document', models.ForeignKey(help_text='Select or upload a PDF document. It is IMPORTANT to limit these documents to PDFs - otherwise the mobile app may not be able to display them properly.', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtaildocs.document')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='content.contentitem')),
            ],
            options={
                'unique_together': {('page', 'document')},
            },
        ),
        migrations.CreateModel(
            name='ContentItemGalleryImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('caption', models.CharField(blank=True, max_length=250)),
                ('image', models.ForeignKey(help_text='Select or upload an image. Most of these images will be viewed on mobile devices. The ideal image should be large enough to render clearly on high end mobile devices but not so large that it costs a lot of bandwidth to download. One good size guideline to aim for is 800x1200 pixels. This is a guideline, not an iron-clad rule.', on_delete=django.db.models.deletion.PROTECT, related_name='+', to='wagtailimages.image')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery_images', to='content.contentitem')),
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
                ('intro', wagtail.core.fields.RichTextField(default='myCareHub', help_text="The content site's tagline")),
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
                ('featured_media', models.ForeignKey(help_text='Select or upload an audio or video file. In order to maximize compatibility, please stick to common audio/video formats. For video, H264 encoded MP4 files are recommended. For audio, AAC (Advanced Audio Codec) files are recommended. ', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailmedia.media')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='featured_media', to='content.contentitem')),
            ],
            options={
                'unique_together': {('page', 'featured_media')},
            },
        ),
        migrations.CreateModel(
            name='ContentItemQuestionnaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='questionnaires', to='content.contentitem')),
            ],
            options={
                'unique_together': {('page',)},
            },
        ),
        migrations.CreateModel(
            name='ContentItemTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(help_text='Associated content item', on_delete=django.db.models.deletion.CASCADE, related_name='tagged_items', to='content.contentitem')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='content_contentitemtag_items', to='taggit.tag')),
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
                ('content_item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='content.contentitem')),
                ('organisation', models.ForeignKey(default=mycarehub.users.models.default_organisation, on_delete=django.db.models.deletion.PROTECT, related_name='content_contentlike_related', to='common.organisation')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'content_item')},
            },
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
                ('content_item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='content.contentitem')),
                ('organisation', models.ForeignKey(default=mycarehub.users.models.default_organisation, on_delete=django.db.models.deletion.PROTECT, related_name='content_contentshare_related', to='common.organisation')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'content_item')},
            },
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
                ('content_item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='content.contentitem')),
                ('organisation', models.ForeignKey(default=mycarehub.users.models.default_organisation, on_delete=django.db.models.deletion.PROTECT, related_name='content_contentview_related', to='common.organisation')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'content_item')},
            },
            managers=[
                ('objects', mycarehub.common.models.base_models.AbstractBaseManager()),
            ],
        ),
        migrations.DeleteModel(
            name='HomePage',
        ),
        migrations.AddField(
            model_name='contentitem',
            name='categories',
            field=modelcluster.fields.ParentalManyToManyField(help_text="These are fixed categories (picked from a list set up by the system administrators) that determine what content is presented to readers e.g only content in the 'welcome' category will be shown as welcome content. Each content item must have at least one category.", to='content.ContentItemCategory'),
        ),
        migrations.AddField(
            model_name='contentitem',
            name='hero_image',
            field=models.ForeignKey(blank=True, help_text='An optional banner image. When present, it will be displayed above the content e.g above the article. This makes sense mostly for text articles.', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='content_hero_image', to='wagtailimages.image'),
        ),
        migrations.AddField(
            model_name='contentitem',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(help_text='These are labels that you can apply to the content on the basis of your editorial policy. You need to define at least one tag. The choice of tag(s) should be guided by your editorial manual i.e the decisions that have been made about how to label content. ', through='content.ContentItemTag', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='contentbookmark',
            name='content_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='content.contentitem'),
        ),
        migrations.AddField(
            model_name='contentbookmark',
            name='organisation',
            field=models.ForeignKey(default=mycarehub.users.models.default_organisation, on_delete=django.db.models.deletion.PROTECT, related_name='content_contentbookmark_related', to='common.organisation'),
        ),
        migrations.AddField(
            model_name='contentbookmark',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='contentbookmark',
            unique_together={('user', 'content_item')},
        ),
    ]