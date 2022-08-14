from django.contrib import admin

from .models import VideoAllProxy, VideoPublishedProxy


# Register your models here.


class VideoAllAdmin(admin.ModelAdmin):
    list_display = ["title", "id", "video_id", "state", "is_published", "get_playlist_ids"]
    list_filter = ["state"]
    search_fields = ["title"]
    readonly_fields = ["id", "is_published", "publish_timestamp"]

    class Meta:
        model = VideoAllProxy


admin.site.register(VideoAllProxy, VideoAllAdmin)


class VideoPublishedProxyAdmin(admin.ModelAdmin):
    list_display = ["title", "video_id"]
    search_fields = ["title"]

    class Meta:
        model = VideoPublishedProxy

    def get_queryset(self, request):
        self.filter = VideoPublishedProxy.objects.filter(active=True)
        return self.filter


admin.site.register(VideoPublishedProxy, VideoPublishedProxyAdmin)
