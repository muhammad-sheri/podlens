from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

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
            # Without this the ORM raises ValueError on a non-numeric id and the
            # request 500s; a bad filter value is a client error, not a crash.
            if not podcast_id.isdigit():
                raise ValidationError({"podcast": "Must be a numeric podcast id."})
            qs = qs.filter(podcast_id=podcast_id)
        return qs
