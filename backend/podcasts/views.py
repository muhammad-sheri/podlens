from rest_framework import viewsets

from .models import Episode, Podcast
from .serializers import EpisodeSerializer, PodcastSerializer


class PodcastViewSet(viewsets.ModelViewSet):
    serializer_class = PodcastSerializer
    queryset = Podcast.objects.all()


class EpisodeViewSet(viewsets.ModelViewSet):
    serializer_class = EpisodeSerializer

    def get_queryset(self):
        qs = Episode.objects.all()
        podcast_id = self.request.query_params.get("podcast")
        if podcast_id:
            qs = qs.filter(podcast_id=podcast_id)
        return qs
