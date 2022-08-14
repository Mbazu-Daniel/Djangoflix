# Generated by Django 3.2.14 on 2022-08-14 19:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0008_alter_video_video_id'),
        ('playlists', '0003_auto_20220814_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='featured_playlist', to='videos.video'),
        ),
    ]