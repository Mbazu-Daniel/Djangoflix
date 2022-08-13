from django.db import models
from django.utils import timezone
# Create your models here.
class Video(models.Model):
    class VideoStateOptions(models.TextChoices):
        # Constant = database_value, user_display value
        PUBLISH = 'PU', "Publish"
        DRAFT = 'DR', "Draft"


    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    video_id = models.CharField(max_length= 200)
    active = models.BooleanField(default = True)
    # timestamp
    # updated 
    state = models.CharField(max_length = 2, choices = VideoStateOptions.choices, default = VideoStateOptions.DRAFT)
    publish_timestamp = models.DateTimeField(auto_now_add = False, auto_now = False, blank = True, null = True)

    # Customize the name active to published on the admin panel
    @property
    def is_published(self):
        return self.active

    def save(self, *args, **kwargs):
        if(self.state == self.VideoStateOptions.PUBLISH and self.publish_timestamp is None):
            print("save as timestamp  for published")
            self.publish_timestamp = timezone.now()
        elif self.state == self.VideoStateOptions.DRAFT:
            self.publish_timestamp = None
            super().save(*args, **kwargs)

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