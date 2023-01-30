# Generated by Django 3.2.16 on 2023-01-30 18:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0004_auto_20230130_2134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contentitemmedialink',
            name='featured_media',
            field=models.ForeignKey(help_text='Select or upload an audio or video file. In order to maximize compatibility, please stick to common audio/video formats. For video, H264 encoded MP4 files are recommended. For audio, AAC (Advanced Audio Codec) files are recommended. ', on_delete=django.db.models.deletion.CASCADE, related_name='content_item_media', to='content.custommedia'),
        ),
    ]
