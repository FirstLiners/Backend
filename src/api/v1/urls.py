from django.urls import include, path
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView

urlpatterns = [
    path("", include("api.v1.skus.urls")),
    path("", include("api.v1.stores.urls")),
    path("", include("api.v1.sales.urls")),
    path("", include("api.v1.forecasts.urls")),
    path("users/", include("api.v1.users.urls")),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"
    ),
]
