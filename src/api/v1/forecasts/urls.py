from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ForecastPostViewSet,
    ForecastViewSet,
    StatisticsViewset,
    StoreSKUViewSet,
)

forecasts_router = DefaultRouter()

forecasts_router.register(
    "load_forecasts", ForecastPostViewSet, basename="load_forecasts"
)
forecasts_router.register("forecasts", ForecastViewSet, basename="forecasts")
forecasts_router.register(
    "statistics", StatisticsViewset, basename="statistics"
)
forecasts_router.register("forecast_data", StoreSKUViewSet, "forecast_data")

urlpatterns = [
    path("", include(forecasts_router.urls)),
]
