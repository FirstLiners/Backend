from datetime import timedelta

from django.db.models import F, Max, Sum
from django.db.models.functions import Abs
from django.http import HttpResponse
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from forecasts.models import Forecast

from .filters import ForecastFilter, StatisticsFilter
from .serializers import ForecastSerializer, StatisticsSerializer
from .services import forecast_file_creation, statistics_file_creation


@extend_schema(tags=["Forecast Info"])
@extend_schema_view(
    list=extend_schema(summary="Информация о прогнозах продаж товара в ТЦ"),
)
class ForecastViewset(ListModelMixin, GenericViewSet):
    """
    Вьюсет для вывода прогноза продаж.
    """

    serializer_class = ForecastSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ForecastFilter

    def get_queryset(self):
        return Forecast.objects.values(
            "store__store_id",
            "sku__sku_id",
            "sku__subcategory__subcat_id",
            "sku__subcategory__category__cat_id",
            "sku__subcategory__category__group__group_id",
            "sku__uom",
            "forecast_data",
        ).annotate(date=Max("date"))

    @extend_schema(
        summary=("Выгрузить прогноз в excel. Параметры как в запросе list."),
        methods=["GET"],
    )
    @action(
        detail=False,
        methods=["get"],
        url_path="download_actual_forecast",
    )
    def download_actual_forecast(self, request):
        """
        Выгрузка актуального прогоноза в excel.
        """
        forecasts = self.filter_queryset(self.get_queryset())
        file = forecast_file_creation(forecasts)
        return HttpResponse(
            file,
            headers={
                "Content-Type": "application/vnd.ms-excel",
                "Content-Disposition": 'attachment; filename="forecast.xls"',
            },
        )


@extend_schema(tags=["Statistics"])
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
                    "sku__uom",
                    "sku__subcategory__subcat_id",
                    "sku__subcategory__category__cat_id",
                    "sku__subcategory__category__group__group_id",
                    field,
                )
                .annotate(
                    forecast=Sum("next_day_forecast"),
                    real_sale=Sum("next_day_real_sale"),
                    period=F(field),
                    difference=(
                        Sum("next_day_real_sale") - Sum("next_day_forecast")
                    ),
                    wape=(
                        (
                            Sum(
                                Abs(
                                    F("next_day_real_sale")
                                    - F("next_day_forecast")
                                )
                            )
                            / Sum("next_day_real_sale")
                        )
                    ),
                )
                .filter(
                    date__lte=timezone.now().date(),
                    date__gte=timezone.now().date()
                    - timedelta(days=Periods.get(period, Periods["day"])),
                )
            )
        return queryset

    @extend_schema(
        summary=(
            "Выгрузить статистику в excel. Параметры как в запросе list."
        ),
        methods=["GET"],
    )
    @action(
        detail=False,
        methods=["get"],
        url_path="download_statistics",
    )
    def download_statistics(self, request):
        """
        Выгрузка статистики по прогонозам в excel.
        """

        ststistics = self.filter_queryset(self.get_queryset())
        file = statistics_file_creation(ststistics)
        return HttpResponse(
            file,
            headers={
                "Content-Type": "application/vnd.ms-excel",
                "Content-Disposition": 'attachment; filename="statistics.xls"',
            },
        )
