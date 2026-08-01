from django.conf import settings
from django.http import JsonResponse
from django.urls import include, path


def health(_request):
    return JsonResponse({"status": "ok", "service": "podlens-api"})


def index(request):
    """Root index, so hitting the API host explains itself instead of 404ing."""
    url = request.build_absolute_uri
    return JsonResponse(
        {
            "service": "podlens-api",
            "dashboard": settings.FRONTEND_ORIGIN,
            "authentication": "none",
            "note": "Every endpoint below is open. Keep this host private.",
            "endpoints": {
                "health": url("/api/health"),
                "podcasts": url("/api/podcasts/"),
                "episodes": url("/api/episodes/"),
                "analytics_overview": url("/api/analytics/overview"),
                "analytics_platforms": url("/api/analytics/platforms"),
                "analytics_episodes": url("/api/analytics/episodes"),
                "insights_generate": {
                    "method": "POST",
                    "url": url("/api/insights/generate"),
                },
            },
        },
        json_dumps_params={"indent": 2},
    )


urlpatterns = [
    path("", index),
    path("api/health", health),
    path("api/", include("podcasts.urls")),
    path("api/analytics/", include("analytics.urls")),
    path("api/insights/", include("insights.urls")),
]
