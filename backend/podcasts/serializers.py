from rest_framework import serializers

from .models import Episode, Podcast


class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = (
            "id",
            "podcast",
            "title",
            "published_at",
            "duration_seconds",
        )


class PodcastSerializer(serializers.ModelSerializer):
    episode_count = serializers.IntegerField(source="episodes.count", read_only=True)

    class Meta:
        model = Podcast
        fields = (
            "id",
            "title",
            "description",
            "cover_url",
            "platforms",
            "episode_count",
            "created_at",
        )
        read_only_fields = ("created_at",)
