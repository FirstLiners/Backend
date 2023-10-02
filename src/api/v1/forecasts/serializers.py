from rest_framework import serializers

from forecasts.models import Forecast


class ForecastGetSerializer(serializers.ModelSerializer):
    """
    Сериализатор для прогнозов по продажам.
    """

    sku_id = serializers.CharField(source="sku.sku_id")
    store_id = serializers.CharField(source="store.store_id")

    class Meta:
        model = Forecast
        fields = (
            "store_id",
            "sku_id",
            "date",
            "forecast_data",
        )
