from rest_framework.response import Response
from rest_framework.views import APIView

from analytics import queries
from podcasts.models import Podcast

from .claude_client import generate_insight


class GenerateInsightView(APIView):
    def post(self, request):
        podcast_ids = list(
            Podcast.objects.filter(owner=request.user).values_list("id", flat=True)
        )
        summary_stats = {
            **queries.overview(podcast_ids),
            "platforms": queries.by_platform(podcast_ids),
        }
        return Response(generate_insight(summary_stats))
