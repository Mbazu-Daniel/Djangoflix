from Djangoflix.db.models import PublishStateOptions
from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify

from .models import Video


# Create your tests here.


class VideoModelTestCase(TestCase):
    def setUp(self):
        self.obj_a = Video.objects.create(title="This is my title", video_id="dafa")
        self.obj_b = Video.objects.create(
            title="This is my title2", state=PublishStateOptions.PUBLISH, video_id="daf"
        )

    def test_valid_title(self):
        title = "This is my title"
        qs = Video.objects.filter(title=title)
        self.assertTrue(qs.exists())

    def test_count_videos(self):
        qs = Video.objects.all()
        self.assertEqual(qs.count(), 2)

    def test_draft_videos(self):
        qs = Video.objects.filter(state=PublishStateOptions.DRAFT)
        self.assertEqual(qs.count(), 1)

    def test_publish_videos(self):
        now = timezone.now()
        published_qs = Video.objects.filter(
            state=PublishStateOptions.PUBLISH, publish_timestamp__lte=now
        )
        self.assertTrue(published_qs.exists())

    def test_publish_manager(self):
        published_qs = Video.objects.all().published()
        published_qs_2 = Video.objects.published()
        self.assertTrue(published_qs.exists())
        self.assertEqual(published_qs.count(), published_qs_2.count())

    def test_slug_field(self):
        title = self.obj_a.title
        test_slug = slugify(title)
        self.assertEqual(
            test_slug, self.obj_a.slug
        )  # to learn how to make a better slug, check out DJANGO MODELS Unleashed
