from datetime import timedelta

from django.db.models import F, Max, Sum
from django.http import HttpResponse
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from forecasts.models import Forecast

from .filters import ForecastFilter, StatisticsFilter
from .serializers import ForecastInfoSerializer, StatisticsSerializer
from .services import forecast_file_creation


@extend_schema(tags=["Forecast Info"])
@extend_schema_view(
    list=extend_schema(summary="Информация о прогнозах продаж товара в ТЦ"),
)
class ForecastViewset(ListModelMixin, GenericViewSet):
    """
    Вьюсет для вывода прогноза продаж.
    """

    serializer_class = ForecastInfoSerializer
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


@extend_schema(tags=["Forecasts statistics"])
@extend_schema_view(
    list=extend_schema(summary="Информация о качестве прогноза"),
)
class StatisticsViewset(ListModelMixin, GenericViewSet):
    """
    Вьюсет для вывода статистики по прогнозам.
    Принимает параметр "period" со значениями:
    "day"(значение по умолчанию, выводит статистику за 14 предыдущих дней
    с разбивкой по дням);
    "week" (выводит статистику за 7 предыдущих недель с разбивкой по неделям);
    "month" (выводит статистику за год с разбивкой по месяцам).
    """

    serializer_class = StatisticsSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = StatisticsFilter

    def get_queryset(self):
        Periods = {
            "day": 14,
            "week": 49,
            "month": 365,
        }
        queryset = Forecast.objects.none()
        if self.request.method == "GET":
            params = self.request.query_params
            period = params.get("period", "day")
            if period not in Periods.keys():
                period = "day"
            field = f"date__{period}"
            queryset = (
                Forecast.objects.values(
                    "store__store_id",
                    "sku__sku_id",
                    field,
                )
                .annotate(
                    forecast=Sum("next_day_forecast"),
                    real_sale=Sum("next_day_real_sale"),
                    period=F(field),
                )
                .filter(
                    date__lte=timezone.now().date(),
                    date__gte=timezone.now().date()
                    - timedelta(days=Periods.get(period, Periods["day"])),
                )
            )
        return queryset
