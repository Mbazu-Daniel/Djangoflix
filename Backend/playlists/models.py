from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from Djangoflix.db.models import PublishStateOptions
from Djangoflix.db.receivers import publish_state_pre_save, slugify_pre_save
from videos.models import Video
# Create your models here.
""" This class is running a query on the database for Playlists that are published and has the correct timestamp"""
class PlaylistQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(
            state=PublishStateOptions.PUBLISH, publish_timestamp__lte=now
        )


""" This class manages the published query from the database"""
class PlaylistManager(models.Manager):
    def get_queryset(self):
        return PlaylistQuerySet(
            self.model, using=self._db
        )  # self._db means using our current database

    def published(self):
        return self.get_queryset().published()


class Playlist(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    video = models.ForeignKey(Video,blank=True, null = True, on_delete = models.SET_NULL, related_name= "playlist_featured")
    videos = models.ManyToManyField(Video,blank=True, related_name= "playlist_item" )
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    state = models.CharField(
        max_length=2,
        choices=PublishStateOptions.choices,
        default=PublishStateOptions.DRAFT,
    )
    publish_timestamp = models.DateTimeField(
        auto_now_add=False, auto_now=False, blank=True, null=True
    )
    objects = PlaylistManager()
    # Customize the name active to published on the admin panel
    @property
    def is_published(self):
        return self.active


pre_save.connect(publish_state_pre_save, sender=Playlist)

pre_save.connect(slugify_pre_save, sender=Playlist)
