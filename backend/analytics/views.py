from rest_framework.response import Response
from rest_framework.views import APIView

from podcasts.models import Episode, Podcast

from . import queries


def _podcast_ids():
    return list(Podcast.objects.values_list("id", flat=True))


class OverviewView(APIView):
    def get(self, request):
        return Response(queries.overview(_podcast_ids()))


class PlatformsView(APIView):
    def get(self, request):
        return Response(queries.by_platform(_podcast_ids()))


class EpisodesView(APIView):
    """Per-episode rollups, joined with episode titles from Postgres."""

    def get(self, request):
        rows = queries.by_episode(_podcast_ids())
        titles = dict(Episode.objects.values_list("id", "title"))
        for row in rows:
            row["title"] = titles.get(row["episode_id"], "Unknown episode")
        return Response(rows)
