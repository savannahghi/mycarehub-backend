# Generated by Django 3.2.16 on 2023-01-31 08:50

import django.db.models.deletion
import taggit.managers
import wagtail.models.collections
import wagtail.search.index
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailcore", "0078_referenceindex"),
        ("taggit", "0004_alter_taggeditem_content_type_alter_taggeditem_tag"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("common", "0005_alter_program_facilities"),
        ("content", "0005_alter_contentitemmedialink_featured_media"),
    ]

    operations = [
        migrations.CreateModel(
            name="CustomDocument",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="title")),
                ("file", models.FileField(upload_to="documents", verbose_name="file")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="created at")),
                ("file_size", models.PositiveIntegerField(editable=False, null=True)),
                ("file_hash", models.CharField(blank=True, editable=False, max_length=40)),
                (
                    "collection",
                    models.ForeignKey(
                        default=wagtail.models.collections.get_root_collection_id,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="wagtailcore.collection",
                        verbose_name="collection",
                    ),
                ),
                (
                    "organisation",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="content_customdocument_related",
                        to="common.organisation",
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        blank=True,
                        help_text=None,
                        through="taggit.TaggedItem",
                        to="taggit.Tag",
                        verbose_name="tags",
                    ),
                ),
                (
                    "uploaded_by_user",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="uploaded by user",
                    ),
                ),
            ],
            options={
                "verbose_name": "document",
                "verbose_name_plural": "documents",
                "abstract": False,
            },
            bases=(wagtail.search.index.Indexed, models.Model),
        ),
        migrations.AlterField(
            model_name="contentitemdocumentlink",
            name="document",
            field=models.ForeignKey(
                help_text="Select or upload a PDF document. It is IMPORTANT to limit these documents to PDFs - otherwise the mobile app may not be able to display them properly.",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="content_item_documents",
                to="content.customdocument",
            ),
        ),
    ]
