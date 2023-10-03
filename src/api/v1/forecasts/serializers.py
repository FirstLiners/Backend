from rest_framework import serializers

from forecasts.models import Forecast


class ForecastGetSerializer(serializers.ModelSerializer):
    """
    Сериализатор для прогнозов по продажам.
    """

    sku = serializers.CharField(source="sku__sku_id")
    store = serializers.CharField(source="store__store_id")

    class Meta:
        model = Forecast
        fields = (
            "store",
            "sku",
            "date",
            "forecast_data",
        )
