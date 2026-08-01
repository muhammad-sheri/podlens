from django.db import models

PLATFORMS = ("spotify", "youtube", "apple")


class Podcast(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    cover_url = models.URLField(blank=True)
    # Comma-separated list of platforms this show is distributed on.
    platforms = models.CharField(max_length=255, default="spotify,youtube,apple")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Episode(models.Model):
    podcast = models.ForeignKey(
        Podcast, on_delete=models.CASCADE, related_name="episodes"
    )
    title = models.CharField(max_length=255)
    published_at = models.DateField()
    duration_seconds = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title
