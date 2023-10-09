from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import StoreViewSet


stores_router = DefaultRouter()

stores_router.register("stores", StoreViewSet, basename="stores")

urlpatterns = [
    path("", include(stores_router.urls)),
]
