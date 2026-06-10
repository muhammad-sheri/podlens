from django.urls import path

from .views import GenerateInsightView

urlpatterns = [
    path("generate", GenerateInsightView.as_view(), name="insights-generate"),
]
