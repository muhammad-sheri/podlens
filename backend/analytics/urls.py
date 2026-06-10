from django.urls import path

from .views import EpisodesView, OverviewView, PlatformsView

urlpatterns = [
    path("overview", OverviewView.as_view(), name="analytics-overview"),
    path("platforms", PlatformsView.as_view(), name="analytics-platforms"),
    path("episodes", EpisodesView.as_view(), name="analytics-episodes"),
]
