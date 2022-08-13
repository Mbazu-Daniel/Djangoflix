from django.db import models

# Create your models here.
class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    video_id = models.CharField(max_length= 200)
    active = models.BooleanField(default = True)
    # timestamp
    # updated 
    # state
    # publish_timestamp

    # Customize the name active to published on the admin panel
    @property
    def is_published(self):
        return self.active

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