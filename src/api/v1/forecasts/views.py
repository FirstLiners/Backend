from datetime import timedelta

from django.db.models import F, Max, Sum
from django.db.models.functions import Abs
from django.http import HttpResponse
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiExample,
)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from forecasts.models import Forecast, StoreSKU

from .filters import ForecastFilter, StatisticsFilter, StoreSKUFilter
from .serializers import (
    ForecastCreateSerializer,
    ForecastSerializer,
    StatisticsSerializer,
    StoreSKUSerializer,
)
from .services import forecast_file_creation, statistics_file_creation


@extend_schema(tags=["Forecasts"])
@extend_schema_view(
    create=extend_schema(
        summary="Загрузка данных по прогнозам",
        examples=[
            OpenApiExample(
                "Пример загрузки данных",
                value=[
                    {
                        "store": "084a8a9aa8cced9175bd07bc44998e75",
                        "sku": "002c3a40ac50dc870f1ff386f11f5bae",
                        "date": "2023-10-05",
                        "forecast_data": {
                            "2023-10-03": 1,
                            "2023-10-04": 3,
                            "2023-10-05": 7,
                            "2023-10-06": 9,
                            "2023-10-07": 0,
                            "2023-10-08": 1,
                            "2023-10-09": 3,
                            "2023-10-10": 7,
                            "2023-10-11": 9,
                            "2023-10-12": 0,
                            "2023-10-13": 1,
                            "2023-10-14": 1,
                            "2023-10-15": 3,
                        },
                    },
                ],
                status_codes=[str(status.HTTP_201_CREATED)],
            ),
        ],
    ),
)
class ForecastPostViewSet(CreateModelMixin, GenericViewSet):
    """
    Вьюсет для загрузки прогнозов.
    """

    serializer_class = ForecastCreateSerializer
    queryset = Forecast.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = ForecastCreateSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)


@extend_schema(tags=["Forecasts"])
@extend_schema_view(
    list=extend_schema(summary="Информация о прогнозах продаж товара в ТЦ"),
)
class ForecastViewSet(ListModelMixin, GenericViewSet):
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
            "day": 16,
            "week": 51,
            "month": 367,
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
                                    F("next_day_real_sale") * 100
                                    - F("next_day_forecast") * 100
                                )
                            )
                            / Sum("next_day_real_sale")
                        )
                    ),
                )
                .filter(
                    date__lte=timezone.now().date() - timedelta(days=2),
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


@extend_schema(tags=["Stores&Skus"])
@extend_schema_view(
    list=extend_schema(
        summary="Пары магазин-товар, покоторым нужно сделать прогноз"
    ),
)
class StoreSKUViewSet(ListModelMixin, GenericViewSet):
    """
    Вьюсет для пар магазин/товар, по которым нужн прогноз.
    """

    serializer_class = StoreSKUSerializer
    queryset = StoreSKU.objects.filter(is_active=True)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = StoreSKUFilter
