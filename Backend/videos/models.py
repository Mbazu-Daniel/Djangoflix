from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from Djangoflix.db.models import PublishStateOptions
from Djangoflix.db.receivers import publish_state_pre_save, slugify_pre_save

# Create your models here.
""" This class is running a query on the database for videos that are published and has the correct timestamp"""


class VideoQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(
            state=PublishStateOptions.PUBLISH, publish_timestamp__lte=now
        )


""" This class manages the published query from the database"""


class VideoManager(models.Manager):
    def get_queryset(self):
        return VideoQuerySet(
            self.model, using=self._db
        )  # self._db means using our current database

    def published(self):
        return self.get_queryset().published()


class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    video_id = models.CharField(max_length=200, unique=True)
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
    objects = VideoManager()
    # Customize the name active to published on the admin panel
    @property
    def is_published(self):
        return self.active

    # getting a reversed relationship for the playlist
    def get_playlist_ids(self):
        return list(self.playlist_featured.all().values_list("id", flat=True))


""" This model is a proxy model to monitor our published videos"""


class VideoAllProxy(Video):
    class Meta:
        proxy = True
        verbose_name = "All Video"
        verbose_name_plural = "All Videos"


""" This model is a proxy model to monitor our published videos"""


class VideoPublishedProxy(Video):
    class Meta:
        proxy = True
        verbose_name = "Published Video"
        verbose_name_plural = "Published Videos"


pre_save.connect(publish_state_pre_save, sender=Video)

pre_save.connect(slugify_pre_save, sender=Video)
