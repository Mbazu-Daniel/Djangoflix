from Djangoflix.db.models import PublishStateOptions
from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify

from .models import Playlist
from videos.models import Video

# Create your tests here.


class PlaylistModelTestCase(TestCase):
    def create_videos(self):
        video_a = Video.objects.create(title="This is my title", video_id="dafa")
        video_b = Video.objects.create(title="This is my title2", video_id="daf")
        video_c = Video.objects.create(title="This is my title", video_id="dafca")
        self.video_a = video_a
        self.video_b = video_b
        self.video_c = video_c

    def setUp(self):
        self.create_videos()
        self.obj_a = Playlist.objects.create(title="This is my title",video = self.video_a )
        obj_b = Playlist.objects.create(
            title="This is my title2", state=PublishStateOptions.PUBLISH,video = self.video_b)
        # obj_b.videos.set([self.video_a, self.video_b, self.video_c])
        v_qs = Video.objects.all()
        obj_b.videos.set(v_qs)
        obj_b.save()
        self.obj_b = obj_b

    def test_playlist_video(self):
        self.assertEqual(self.obj_a.video, self.video_a)

    def test_playlist_video_items(self):
        count = self.obj_b.videos.all().count()
        self.assertEqual(count, 3)

    def test_video_playlist(self):
        qs = self.video_a.playlist_featured.all()
        self.assertEqual(qs.count(), 1)

    def test_video_playlist_ids_property(self):
        ids = self.video_a.get_playlist_ids()
        actual_ids = list(Playlist.objects.filter(video=self.video_a).values_list("id", flat=True))
        self.assertEqual(ids, actual_ids)


    def test_valid_title(self):
        title = "This is my title"
        qs = Playlist.objects.filter(title=title)
        self.assertTrue(qs.exists())

    def test_count_Playlists(self):
        qs = Playlist.objects.all()
        self.assertEqual(qs.count(), 2)

    def test_draft_Playlists(self):
        qs = Playlist.objects.filter(state=PublishStateOptions.DRAFT)
        self.assertEqual(qs.count(), 1)

    def test_publish_Playlists(self):
        now = timezone.now()
        published_qs = Playlist.objects.filter(
            state=PublishStateOptions.PUBLISH, publish_timestamp__lte=now
        )
        self.assertTrue(published_qs.exists())

    def test_publish_manager(self):
        published_qs = Playlist.objects.all().published()
        published_qs_2 = Playlist.objects.published()
        self.assertTrue(published_qs.exists())
        self.assertEqual(published_qs.count(), published_qs_2.count())

    def test_slug_field(self):
        title = self.obj_a.title
        test_slug = slugify(title)
        self.assertEqual(
            test_slug, self.obj_a.slug
        )  # to learn how to make a better slug, check out DJANGO MODELS Unleashed
