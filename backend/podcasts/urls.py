from rest_framework.routers import DefaultRouter

from .views import EpisodeViewSet, PodcastViewSet

router = DefaultRouter()
router.register("podcasts", PodcastViewSet, basename="podcast")
router.register("episodes", EpisodeViewSet, basename="episode")

urlpatterns = router.urls
