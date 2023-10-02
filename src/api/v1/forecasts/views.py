from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from forecasts.models import Forecast

from .serializers import ForecastGetSerializer


@extend_schema(tags=["Forecasts"])
@extend_schema_view(
    list=extend_schema(summary="Информация о прогнозах продаж товара в ТЦ"),
)
class ForecastViewset(ListModelMixin, GenericViewSet):
    """
    Вьюсет для прогнозов продаж.
    """

    queryset = Forecast.objects.all()
    serializer_class = ForecastGetSerializer
