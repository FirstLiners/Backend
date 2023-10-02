from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ForecastViewset

forecasts_router = DefaultRouter()

forecasts_router.register("forecasts", ForecastViewset, basename="forecasts")

urlpatterns = [
    path("", include(forecasts_router.urls)),
]
