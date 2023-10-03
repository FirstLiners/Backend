from django.db.models import Max
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny

from forecasts.models import Forecast

from .filters import ForecastFilter
from .serializers import ForecastGetSerializer
from .services import forecast_file_creation


@extend_schema(tags=["Forecasts"])
@extend_schema_view(
    list=extend_schema(summary="Информация о прогнозах продаж товара в ТЦ"),
)
class ForecastViewset(ListModelMixin, GenericViewSet):
    """
    Вьюсет для прогнозов продаж.
    """

    serializer_class = ForecastGetSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ForecastFilter

    def get_queryset(self):
        return Forecast.objects.values(
            "store__store_id", "sku__sku_id", "forecast_data"
        ).annotate(date=Max("date"))

    @action(
        detail=False,
        methods=["get"],
        url_path="download_actual_forecast",
        permission_classes=(AllowAny,),
    )
    def download_actual_forecast(self, request):
        """
        Загрузка актуального прогноза.
        """
        forecasts = Forecast.objects.values(
            "store__store_id",
            "sku__sku_id",
            "sku__subcategory__subcat_id",
            "sku__subcategory__category__cat_id",
            "sku__subcategory__category__group__group_id",
            "forecast_data",
        ).annotate(date=Max("date"))
        file = forecast_file_creation(forecasts)
        return HttpResponse(
            file,
            headers={
                "Content-Type": "application/vnd.ms-excel",
                "Content-Disposition": 'attachment; filename="forecast.xls"',
            },
        )
