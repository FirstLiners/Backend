from rest_framework import serializers

from forecasts.models import Forecast


class ForecastInfoSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода прогноз по продажам.
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


class StatisticsListSerializer(serializers.ListSerializer):
    """
    Сериализатор для вывода статистики по прогнозам,
    объединенной по паре товар - магазин.
    """

    def to_representation(self, data):
        statistic = []
        for forecast in range(0, len(data)):
            info = {
                "store": data[forecast]["store__store_id"],
                "sku": data[forecast]["sku__sku_id"],
                "data": [
                    {
                        "real_sale": data[forecast]["real_sale"],
                        "forecast": data[forecast]["forecast"],
                        "period": data[forecast]["period"],
                    }
                ],
            }
            if forecast == 0:
                statistic.append(info)
            else:
                if (
                    statistic[-1]["store"] == data[forecast]["store__store_id"]
                    and statistic[-1]["sku"] == data[forecast]["sku__sku_id"]
                ):
                    statistic[-1]["data"].append(
                        {
                            "real_sale": data[forecast]["real_sale"],
                            "forecast": data[forecast]["forecast"],
                            "period": data[forecast]["period"],
                        }
                    )
                else:
                    statistic.append(info)
        return statistic


class StatisticsSerializer(serializers.Serializer):
    """
    Сериализатор для вывода статистики по прогнозам.
    """

    store = serializers.CharField(source="store__store_id", read_only=True)
    sku = serializers.CharField(source="sku__sku_id", read_only=True)
    forecast = serializers.IntegerField(read_only=True)
    real_sale = serializers.IntegerField(read_only=True)
    period = serializers.IntegerField(read_only=True)

    class Meta:
        fields = (
            "store",
            "sku",
            "real_sale",
            "forecast",
            "period",
        )
        list_serializer_class = StatisticsListSerializer
