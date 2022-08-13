from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify
from .models import Video


# Create your tests here.

class VideoModelTestCase(TestCase):
    def setUp(self):
        self.obj_a = Video.objects.create(title="This is my title", video_id = "dafa")
        self.obj_b = Video.objects.create(title="This is my title2", state=Video.VideoStateOptions.PUBLISH, video_id = "daf")

    def test_valid_title(self):
        title = "This is my title"
        qs = Video.objects.filter(title=title)
        self.assertTrue(qs.exists())

    def test_count_videos(self):
        qs = Video.objects.all()
        self.assertEqual(qs.count(), 2)

    def test_draft_videos(self):
        qs = Video.objects.filter(state=Video.VideoStateOptions.DRAFT)
        self.assertEqual(qs.count(), 1)

    def test_publish_videos(self):
        qs = Video.objects.filter(state=Video.VideoStateOptions.PUBLISH)
        now = timezone.now()
        published_qs = Video.objects.filter(publish_timestamp__lte = now)
        self.assertTrue(published_qs.exists())

    def test_slug_field(self):
        title = self.obj_a.title
        test_slug = slugify(title)
        self.assertEqual(test_slug, self.obj_a.slug)
        # to learn how to make a better slug, check out DJAANGO MODELS Unleashed
