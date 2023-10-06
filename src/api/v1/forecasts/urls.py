from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ForecastViewset, StatisticsViewset

forecasts_router = DefaultRouter()

forecasts_router.register("forecasts", ForecastViewset, basename="forecasts")
forecasts_router.register(
    "statistics", StatisticsViewset, basename="statistics"
)

urlpatterns = [
    path("", include(forecasts_router.urls)),
]
