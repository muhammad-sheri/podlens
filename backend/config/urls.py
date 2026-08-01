from django.http import JsonResponse
from django.urls import include, path


def health(_request):
    return JsonResponse({"status": "ok", "service": "podlens-api"})


urlpatterns = [
    path("api/health", health),
    path("api/", include("podcasts.urls")),
    path("api/analytics/", include("analytics.urls")),
    path("api/insights/", include("insights.urls")),
]
