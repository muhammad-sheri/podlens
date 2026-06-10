from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def health(_request):
    return JsonResponse({"status": "ok", "service": "podlens-api"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health", health),
    path("api/auth/", include("accounts.urls")),
    path("api/", include("podcasts.urls")),
    path("api/analytics/", include("analytics.urls")),
    path("api/insights/", include("insights.urls")),
]
