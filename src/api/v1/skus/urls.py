from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, GroupViewSet, SKUViewSet,
                    SubCategoryViewSet)


skus_router = DefaultRouter()

skus_router.register("skus", SKUViewSet, basename="skus")
skus_router.register("categories", CategoryViewSet, basename="categories")
skus_router.register(
    "subcategories",
    SubCategoryViewSet,
    basename="subcategories")
skus_router.register("groups", GroupViewSet, basename="groups")

urlpatterns = [
    path("", include(skus_router.urls)),
]
