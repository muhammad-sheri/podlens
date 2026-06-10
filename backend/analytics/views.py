from rest_framework.response import Response
from rest_framework.views import APIView

from podcasts.models import Episode, Podcast

from . import queries


def _user_podcast_ids(user):
    return list(Podcast.objects.filter(owner=user).values_list("id", flat=True))


class OverviewView(APIView):
    def get(self, request):
        podcast_ids = _user_podcast_ids(request.user)
        return Response(queries.overview(podcast_ids))


class PlatformsView(APIView):
    def get(self, request):
        podcast_ids = _user_podcast_ids(request.user)
        return Response(queries.by_platform(podcast_ids))


class EpisodesView(APIView):
    """Per-episode rollups, joined with episode titles from Postgres."""

    def get(self, request):
        podcast_ids = _user_podcast_ids(request.user)
        rows = queries.by_episode(podcast_ids)
        titles = dict(
            Episode.objects.filter(podcast__owner=request.user).values_list(
                "id", "title"
            )
        )
        for row in rows:
            row["title"] = titles.get(row["episode_id"], "Unknown episode")
        return Response(rows)
