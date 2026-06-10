from rest_framework import viewsets

from .models import Episode, Podcast
from .serializers import EpisodeSerializer, PodcastSerializer


class PodcastViewSet(viewsets.ModelViewSet):
    serializer_class = PodcastSerializer

    def get_queryset(self):
        return Podcast.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class EpisodeViewSet(viewsets.ModelViewSet):
    serializer_class = EpisodeSerializer

    def get_queryset(self):
        qs = Episode.objects.filter(podcast__owner=self.request.user)
        podcast_id = self.request.query_params.get("podcast")
        if podcast_id:
            qs = qs.filter(podcast_id=podcast_id)
        return qs
