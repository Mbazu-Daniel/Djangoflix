from django.contrib import admin
from .models import VideoAllProxy, VideoPublishedProxy
# Register your models here.

class VideoAllAdmin(admin.ModelAdmin):
    list_display = ['title', 'id', 'video_id', 'is_published']
    list_filter = ['active']
    search_fields = ["title"]
    readonly_fields = ['id', 'is_published']
    class Meta:
        model =  VideoAllProxy



admin.site.register(VideoAllProxy, VideoAllAdmin)


class VideoPublishedProxyAdmin(admin.ModelAdmin):
    list_display = ['title', 'video_id']
    search_fields = ["title"]
    class Meta:
        model =  VideoPublishedProxy

    def get_queryset(self, request):
        return VideoPublishedProxy.objects.filter(active = True)

admin.site.register(VideoPublishedProxy, VideoPublishedProxyAdmin)