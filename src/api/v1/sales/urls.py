from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SaleGetViewset

sales_router = DefaultRouter()

sales_router.register("sales", SaleGetViewset, basename="sales")

urlpatterns = [
    path("", include(sales_router.urls)),
]
