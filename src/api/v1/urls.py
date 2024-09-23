from django.urls import include, path
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
)

from api.v1 import views

v1_router = DefaultRouter()

v1_router.register("skus", views.SKUViewSet, basename="skus")
v1_router.register("categories", views.CategoryViewSet, basename="categories")
v1_router.register(
    "subcategories", views.SubCategoryViewSet, basename="subcategories"
)
v1_router.register("groups", views.GroupViewSet, basename="groups")
v1_router.register("sales", views.SaleGetViewset, basename="sales")
v1_router.register(
    "load_forecasts", views.ForecastPostViewSet, basename="load_forecasts"
)
v1_router.register("forecasts", views.ForecastViewSet, basename="forecasts")
v1_router.register(
    "statistics", views.StatisticsViewset, basename="statistics"
)
v1_router.register("forecast_data", views.StoreSKUViewSet, "forecast_data")
v1_router.register("stores", views.StoreViewSet, basename="stores")

urlpatterns = [
    path("token/", TokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("logout/", TokenBlacklistView.as_view(), name="token_blacklist"),
    path("", include(v1_router.urls)),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"
    ),
]
